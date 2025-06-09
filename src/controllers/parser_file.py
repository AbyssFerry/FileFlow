import time
from datetime import datetime
from move_file import move_file
from pack_init_file import pack_init_file
import sys
import os
from pathlib import Path
import pandas as pd
from docx import Document
import pdfplumber
import logging

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.controllers_for_ai.ai_processing import FileClassifier
from src.storage.database import folderShow

# Configure logging
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

def parser_file(file_path):
    """
    处理文件并返回移动后的新路径和原因
    
    参数:
        file_path (str): 要处理的文件路径
        
    返回:
        dict: 包含新路径和移动原因的字典
    """
    # 1. 获取文件信息
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    # 获取文件基本信息
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    # 只处理支持的文件类型
    supported_extensions = {'.txt', '.pdf', '.xlsx', '.xls', '.docx'}
    if ext not in supported_extensions:
        raise ValueError(f"不支持的文件类型: {ext}")
    
    # 构建文件信息字典
    file_info = {
        "name": name,
        "absolute_path": os.path.abspath(file_path),
        "extension": ext,
        "created_time": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
        "size": os.path.getsize(file_path),
        "content": "",
        "ai_description": "",
        "short_content": "",
        "reason_for_move": ""
    }

    # 读取文件内容
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                file_info["content"] = f.read()
        elif ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                max_pages = 10  # 只读取前10页
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
        
        # 确保内容不为空
        if not file_info["content"].strip():
            file_info["content"] = "<空文件>"
            
    except Exception as e:
        file_info["content"] = f"<读取错误: {str(e)}>"
        raise RuntimeError(f"读取文件 {file_path} 内容时出错: {str(e)}")

    # 2. 调用AI总结文件
    classifier = FileClassifier()
    try:
        summarized_file = classifier.summary_file(file_info)
        
        # 验证总结结果
        if not summarized_file.get("ai_description") or not summarized_file.get("short_content"):
            raise RuntimeError(f"文件 {file_info['name']} 总结失败，结果不完整")
            
    except Exception as e:
        raise RuntimeError(f"总结文件 {file_info['name']} 时出错: {str(e)}")

    # 3. 获取目录信息
    folds = folderShow()
    
    # 4. 调用AI分类函数
    try:
        fileNewPath = classifier.classify_file(summarized_file, folds)
        
        # 验证分类结果
        if not fileNewPath:
            raise RuntimeError("分类结果无效")
            
    except Exception as e:
        raise RuntimeError(f"分类文件时发生异常: {str(e)}")

    # 5. 初始化文件打包
    try:
        pack_init_file(fileNewPath) 
    except Exception as e:
        raise RuntimeError(f"打包初始文件时出错: {str(e)}")
    
    # 6. 移动文件
    try:
        newPath_and_reason = move_file(fileNewPath)
    except Exception as e:
        raise RuntimeError(f"移动文件时出错: {str(e)}")
     
    # 7. 返回结果
    return newPath_and_reason