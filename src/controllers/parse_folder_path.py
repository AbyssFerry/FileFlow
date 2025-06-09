import os
import sys
from pathlib import Path
import pandas as pd
from docx import Document
import pdfplumber
import logging
from datetime import datetime
from organize_files import organize_files
from pack_init_files import pack_init_files

# 标准化项目根路径为SQL风格
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.storage.database import folderShow
from src.controllers_for_ai.ai_processing import FileClassifier

logging.getLogger("pdfplumber").setLevel(logging.ERROR)

def parse_folder_path(directory: str) -> bool:
    """
    完整的文件处理流程（严格按10个步骤实现）
    所有路径存储使用SQL风格的正斜杠(/)
    只处理 txt, pdf, xlsx, xls, docx 文件
    
    参数:
        directory: 要处理的目录路径（自动转为SQL风格）
        
    返回:
        bool: 处理是否成功
    """
    try:
        # 标准化输入目录路径
        directory = directory.replace('\\', '/')
        
        # === 步骤1: 读取目录并提取文件信息 ===
        file_info_list = []
        supported_extensions = {'.txt', '.pdf', '.xlsx', '.xls', '.docx'}
        
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                # 标准化文件路径
                file_path = os.path.join(root, filename).replace('\\', '/')
                
                # 提取文件基本信息
                name, ext = os.path.splitext(filename)
                ext = ext.lower()
                
                # 跳过不支持的文件类型
                if ext not in supported_extensions:
                    continue
                
                file_info = {
                    "name": name,
                    "absolute_path": os.path.abspath(file_path).replace('\\', '/'),  # 标准化路径
                    "extension": ext,
                    "created_time": datetime.fromtimestamp(
                        os.path.getctime(file_path)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
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
                    
                    if not file_info["content"].strip():
                        file_info["content"] = "<空文件>"
                        
                except Exception as e:
                    file_info["content"] = f"<读取错误: {str(e)}>"
                    print(f"读取文件 {file_path} 内容时出错: {str(e)}")

                file_info_list.append(file_info)

        # === 步骤2-3: 调用AI总结每个文件 ===
        classifier = FileClassifier()
        summarized_files = []
        
        for file_info in file_info_list:
            try:
                if file_info["content"].startswith(("<读取错误:", "<空文件>")):
                    print(f"跳过无效文件: {file_info['name']} - {file_info['content']}")
                    continue

                summarized_file = classifier.summary_file(file_info)
                if not summarized_file.get("ai_description") or not summarized_file.get("short_content"):
                    print(f"文件 {file_info['name']} 总结失败，结果不完整")
                    continue
                    
                summarized_files.append(summarized_file)
                
            except Exception as e:
                print(f"总结文件 {file_info['name']} 时出错: {str(e)}")
                continue

        if not summarized_files:
            print("警告: 没有成功总结任何文件")
            return False

        # === 步骤4-5: 调用AI分类文件 ===
        try:
            classified_files = classifier.classify_files(summarized_files)
            
            # 标准化分类结果中的路径
            for file_info in classified_files["files"]:
                file_info["absolute_path"] = file_info["absolute_path"].replace('\\', '/')
                file_info["new_absolute_path"] = file_info["new_absolute_path"].replace('\\', '/')
                
            for category_info in classified_files["categories"]:
                category_info["absolute_path"] = category_info["absolute_path"].replace('\\', '/')
                
            if not classified_files or not classified_files.get("files") or not classified_files.get("categories"):
                print("错误: 分类结果无效")
                return False
                
        except Exception as e:
            print(f"分类文件时发生异常: {str(e)}")
            return False

        # === 步骤7: 组织文件 ===
        try:
            organize_files(classified_files["files"])
        except Exception as e:
            print(f"组织文件时出错: {str(e)}")
            return False

        # === 步骤8: 补全分类信息 ===
        try:
            for category in classified_files["categories"]:
                category_path = category["absolute_path"]
                if os.path.exists(category_path):
                    stat = os.stat(category_path)
                    category["created_time"] = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                    category["size"] = sum(
                        os.path.getsize(os.path.join(category_path, f))
                        for f in os.listdir(category_path)
                        if os.path.isfile(os.path.join(category_path, f))
                    )
        except Exception as e:
            print(f"补全分类信息时出错: {str(e)}")
            return False

        # === 步骤9: 打包初始文件 ===        
        try:
            pack_init_files(classified_files)
        except Exception as e: 
            print(f"打包初始文件时出错: {str(e)}")
            return False

        return True

    except Exception as e:
        print(f"处理失败: {str(e)}")
        return False