import time
from datetime import datetime
from src.controllers.move_file import move_file
from src.controllers.pack_init_file import pack_init_file
import sys
import os
from pathlib import Path
import pandas as pd
from docx import Document
import pdfplumber
import logging
from src.ui.uiprint import print
from src.controllers_for_ai.ai_processing import FileClassifier
from src.storage.database import folderShow, fileShow

# 标准化项目根路径为SQL风格
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)



# Configure logging
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

def read_doc_file(file_path):
    """
    读取.doc文件内容，使用win32com（Windows）或antiword（跨平台）
    """
    try:
        # 尝试使用win32com（Windows）
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text
        doc.Close()
        word.Quit()
        return text
    except ImportError:
        # 如果win32com不可用，尝试使用antiword
        try:
            from subprocess import Popen, PIPE
            p = Popen(['antiword', file_path], stdout=PIPE)
            stdout, stderr = p.communicate()
            return stdout.decode('utf-8', errors='replace')
        except FileNotFoundError:
            return "请安装antiword或Microsoft Word以支持.doc文件解析"
    except Exception as e:
        return f"<读取错误: {str(e)}>"

def parser_file(file_path, API_KEY: str = ""):
    """
    处理文件并返回移动后的新路径和原因
    所有路径存储使用SQL风格的正斜杠(/)
    
    参数:
        file_path (str): 要处理的文件路径（自动转为SQL风格）
        
    返回:
        dict: 包含新路径和移动原因的字典（路径为SQL风格）
    """
    print(f"\n===== 开始处理文件: {os.path.basename(file_path)} =====")
    
    # 标准化输入文件路径
    file_path = file_path.replace('\\', '/')
    
    # 1. 获取文件信息
    print("步骤1: 获取文件信息...")
    if not os.path.isfile(file_path):
        print(f"错误: 文件不存在: {file_path}")
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 获取文件基本信息（标准化路径）
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    # 只处理支持的文件类型
    supported_extensions = {'.txt', '.pdf', '.xlsx', '.xls', '.docx', '.doc'}
    if ext not in supported_extensions:
        print(f"错误: 不支持的文件类型: {ext}")
        raise ValueError(f"不支持的文件类型: {ext}")
    
    # 构建文件信息字典（使用标准化路径）
    file_info = {
        "name": name,
        "absolute_path": os.path.abspath(file_path).replace('\\', '/'),
        "extension": ext,
        "created_time": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
        "size": os.path.getsize(file_path),
        "content": "",
        "ai_description": "",
        "short_content": "",
        "reason_for_move": ""
    }
    print(f"文件大小: {file_info['size'] / 1024:.2f} KB")

    # 读取文件内容
    print("正在读取文件内容...")
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                file_info["content"] = f.read()
        elif ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                max_pages = 10
                file_info["content"] = "\n".join(
                    page.extract_text() for i, page in enumerate(pdf.pages) 
                    if i < max_pages and page.extract_text()
                )
        elif ext in ('.xlsx', '.xls'):
            file_info["content"] = pd.read_excel(file_path, sheet_name=0).to_string()
        elif ext == '.docx':
            doc = Document(file_path)
            file_info["content"] = "\n".join(
                p.text for p in doc.paragraphs if p.text.strip()
            )
        elif ext == '.doc':
            file_info["content"] = read_doc_file(file_path)
        
        if not file_info["content"].strip():
            file_info["content"] = "<空文件>"
            
    except Exception as e:
        print(f"错误: 读取文件 {file_path} 内容时出错: {str(e)}")
        file_info["content"] = f"<读取错误: {str(e)}>"
        raise RuntimeError(f"读取文件 {file_path} 内容时出错: {str(e)}")
    
    print("步骤1完成: 文件信息已获取")

    # 2. 调用AI总结文件
    print("\n步骤2: 调用AI总结文件内容...")
    classifier = FileClassifier(API_KEY)
    print("AI模型已初始化，开始分析文件...")
    try:
        summarized_file = classifier.summary_file(file_info)
        
        if not summarized_file.get("ai_description") or not summarized_file.get("short_content"):
            print(f"错误: 文件 {file_info['name']} 总结失败，结果不完整")
            raise RuntimeError(f"文件 {file_info['name']} 总结失败，结果不完整")
        
        print("AI总结完成:")
        print(f"- 一句话描述: {summarized_file.get('ai_description', '')[:50]}...")
            
    except Exception as e:
        print(f"错误: 总结文件 {file_info['name']} 时出错: {str(e)}")
        raise RuntimeError(f"总结文件 {file_info['name']} 时出错: {str(e)}")

    # 3. 获取目录信息（确保返回路径标准化）
    print("\n步骤3: 获取目录信息...")
    folds = folderShow()
    if folds:
        for fold in folds:
            if 'absolute_path' in fold:
                fold['absolute_path'] = fold['absolute_path'].replace('\\', '/')
        print(f"已获取 {len(folds)} 个目录信息")
    else:
        print("未找到任何目录信息，将创建新目录")

    # 4. 调用AI分类函数（确保处理标准化路径）
    print("\n步骤4: 调用AI为文件分类...")
    try:
        fileNewPath = classifier.classify_file(summarized_file, folds)
        
        if not fileNewPath:
            print("错误: 分类结果无效")
            raise RuntimeError("分类结果无效")
            
        # 标准化分类结果中的路径
        fileNewPath["absolute_path"] = fileNewPath["absolute_path"].replace('\\', '/')
        fileNewPath["new_absolute_path"] = fileNewPath["new_absolute_path"].replace('\\', '/')
        
        print(f"分类完成: 文件将被移动到 {fileNewPath['new_absolute_path']}")
        print(f"移动原因: {fileNewPath.get('reason_for_move', '无')}")
            
    except Exception as e:
        print(f"错误: 分类文件时发生异常: {str(e)}")
        raise RuntimeError(f"分类文件时发生异常: {str(e)}")

    
    # 5. 移动文件（处理标准化路径）
    print("\n步骤5: 移动文件到分类位置...")
    try:
        newPath_and_reason = move_file(fileNewPath)
        # 确保返回路径标准化
        if 'new_absolute_path' in newPath_and_reason:
            newPath_and_reason['new_absolute_path'] = newPath_and_reason['new_absolute_path'].replace('\\', '/')
        print(f"文件已成功移动到: {newPath_and_reason.get('new_absolute_path', '未知路径')}")
    except Exception as e:
        print(f"错误: 移动文件时出错: {str(e)}")
        raise RuntimeError(f"移动文件时出错: {str(e)}")
     
    # 6. 初始化文件打包（处理标准化路径）
    print("\n步骤6: 初始化文件打包...")
    try:
        pack_init_file(fileNewPath) 
        print("文件打包成功")
        
    except Exception as e:
        print(f"错误: 打包初始文件时出错: {str(e)}")
        raise RuntimeError(f"打包初始文件时出错: {str(e)}")
    # 7. 返回结果（标准化路径）
    print("\n===== 文件处理完成 =====")
    return newPath_and_reason