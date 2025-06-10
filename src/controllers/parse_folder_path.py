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
from parser_file import read_doc_file

# 标准化项目根路径为SQL风格
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.storage.database import folderShow
from src.controllers_for_ai.ai_processing import FileClassifier
import json

logging.getLogger("pdfplumber").setLevel(logging.ERROR)

def scan_directory(directory):
    """扫描目录并统计支持的文件数量"""
    supported_extensions = {'.txt', '.pdf', '.xlsx', '.xls', '.docx', '.doc'}
    total_files = 0
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext.lower() in supported_extensions:
                total_files += 1
    
    return total_files, supported_extensions

def read_file_content(file_path, ext, max_length=1000):
    """读取不同类型文件的内容，去除无效字符后限制最大长度"""
    try:
        content = ""
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        elif ext == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                max_pages = 10
                texts = []
                for i, page in enumerate(pdf.pages):
                    if i >= max_pages:
                        break
                    text = page.extract_text()
                    if text:
                        texts.append(text)
                content = "\n".join(texts)
        elif ext in ('.xlsx', '.xls'):
            content = pd.read_excel(file_path, sheet_name=0).to_string()
        elif ext == '.docx':
            doc = Document(file_path)
            content = "\n".join(
                p.text for p in doc.paragraphs if p.text.strip()
            )
        elif ext == '.doc':
            content = read_doc_file(file_path)
        
        # 去除无效字符（如空白符、不可见字符等）
        if content:
            # 去除所有空白字符（空格、制表符、换行等）和不可见字符
            content = ''.join(c for c in content if not c.isspace() and c.isprintable())

        # 截取最大长度
        if len(content) > max_length:
            content = content[:max_length] + "\n...[后面内容省略]"
        return content
    except Exception as e:
        print(f"读取文件 {file_path} 内容时出错: {str(e)}")
        return ""

def collect_file_info(directory, total_files, supported_extensions):
    """收集目录中所有支持文件的信息"""
    file_info_list = []
    current_file = 0
    
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename).replace('\\', '/')
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # 跳过不支持的文件类型
            if ext not in supported_extensions:
                continue
            
            current_file += 1
            print(f"[{current_file}/{total_files}] 处理文件: {filename}")
            
            file_info = {
                "name": name,
                "absolute_path": os.path.abspath(file_path).replace('\\', '/'),
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
            content = read_file_content(file_path, ext)
            
            if not content.strip():
                file_info["content"] = f"{filename}"            # 如果读取失败，内容设为文件名
            else:
                file_info["content"] = content
            
            # 检查是否包含读取错误信息，如果有则将内容设为文件名
            if content.startswith("<读取错误:") and "很抱歉，找不到您的文件" in content:
                file_info["content"] = f"{filename}"


            # 如果读取失败，内容设为文件名
            if not file_info["content"]:
                file_info["content"] = f"{filename}"
                
            file_info_list.append(file_info)

    # 测试使用@@@@
    # with open(r"D:\vs code\python\FileFlow\testdoc\file_info_list.json", "w", encoding="utf-8") as f:
    #     json.dump(file_info_list, f, ensure_ascii=False, indent=2)

    return file_info_list, current_file

import concurrent.futures

def process_files_with_ai(file_info_list, classifier):
    """使用AI并发处理和总结文件"""
    summarized_files = []
    total_ai_files = len(file_info_list)
    print(f"需要AI总结的文件总数: {total_ai_files}")

    def summarize(file_info_tuple):
        i, file_info = file_info_tuple
        try:
            print(f"[{i+1}/{total_ai_files}] 正在处理: {file_info['name']}{file_info['extension']}")
            if file_info["content"].startswith(("<读取错误:", "<空文件>")):
                print(f"[{i+1}/{total_ai_files}] 跳过无效文件: {file_info['name']} - {file_info['content']}")
                return None
            summarized_file = classifier.summary_file(file_info)
            if not summarized_file.get("ai_description") or not summarized_file.get("short_content"):
                print(f"[{i+1}/{total_ai_files}] 文件 {file_info['name']} 总结失败，结果不完整。")
                return None
            print(f"[{i+1}/{total_ai_files}] 文件 {file_info['name']} 总结完成")
            return summarized_file
        except Exception as e:
            print(f"[{i+1}/{total_ai_files}] 总结文件 {file_info['name']} 时出错: {str(e)}")
            return None
    import os
    # 限制最大线程数为40，避免过多线程导致系统资源耗尽
    max_threads = min(40, (os.cpu_count() or 1) * 2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = list(executor.map(summarize, enumerate(file_info_list)))

    summarized_files = [f for f in results if f is not None]
    print(f"步骤2-3完成: 成功总结了 {len(summarized_files)}/{total_ai_files} 个文件")
    return summarized_files

def classify_and_standardize(summarized_files, classifier):
    """使用AI分类文件并标准化路径"""
    try:
        # 只保留文件名
        path = ''
        for file_info in summarized_files:
            parts = file_info["absolute_path"].split('/')
            file_info["absolute_path"] = parts[-1]
            if not path and len(parts) > 1:
                path = '/'.join(parts[:-1])  # 获取上级目录路径
        
        # 测试@@@
        # print(path)


        # 调用AI分类文件
        classified_files = classifier.classify_files(summarized_files)

        # 给 classified_files["files"] 的路径加上前面路径 path
        for file_info in classified_files["files"]:
            file_info["absolute_path"] = f"{path}/{file_info['absolute_path']}".replace('//', '/')
            file_info["new_absolute_path"] = f"{path}/{file_info['new_absolute_path']}".replace('//', '/')

        # 给 classified_files["categories"] 的路径加上前面路径 path
        for categories_info in classified_files["categories"]:
            categories_info["absolute_path"] = f"{path}/{categories_info['absolute_path']}".replace('//', '/')

        # 输出 summarized_files 到文件@@@@
        # with open(r"D:\vs code\python\FileFlow\testdoc\summarized_files.json", "w", encoding="utf-8") as f:
        #     json.dump(summarized_files, f, ensure_ascii=False, indent=2)

        # 输出 classified_files 到文件@@@@
        # with open(r"D:\vs code\python\FileFlow\testdoc\classified_files.json", "w", encoding="utf-8") as f:
        #     json.dump(classified_files, f, ensure_ascii=False, indent=2)


        # 标准化分类结果中的路径
        for file_info in classified_files["files"]:
            file_info["absolute_path"] = file_info["absolute_path"].replace('\\', '/')
            file_info["new_absolute_path"] = file_info["new_absolute_path"].replace('\\', '/')
            
        for category_info in classified_files["categories"]:
            category_info["absolute_path"] = category_info["absolute_path"].replace('\\', '/')
            
        if not classified_files or not classified_files.get("files") or not classified_files.get("categories"):
            print("错误: 分类结果无效")
            return None
        
        return classified_files
            
    except Exception as e:
        print(f"分类文件时发生异常: {str(e)}")
        return None

def complete_category_info(classified_files):
    """补全分类目录信息"""
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
        return True
    except Exception as e:
        print(f"补全分类信息时出错: {str(e)}")
        return False

def parse_folder_path(directory: str, API_KEY: str = "") -> bool:
    """
    完整的文件处理流程（严格按10个步骤实现）
    所有路径存储使用SQL风格的正斜杠(/)
    只处理 txt, pdf, xlsx, xls, docx, doc 文件
    
    参数:
        directory: 要处理的目录路径（自动转为SQL风格）
        
    返回:
        bool: 处理是否成功
    """
    try:
        # 标准化输入目录路径
        directory = directory.replace('\\', '/')
        
        # === 步骤1: 读取目录并提取文件信息 ===
        print(f"开始步骤1: 读取目录 {directory} 中的文件...")
        
        # 预先统计符合条件的文件总数
        total_files, supported_extensions = scan_directory(directory)
        print(f"共发现 {total_files} 个支持的文件，开始处理...")
        
        # 收集文件信息
        file_info_list, processed_files = collect_file_info(directory, total_files, supported_extensions)
        print(f"步骤1完成: 共处理了 {processed_files} 个文件")

        # 输出 file_info_list 到文件 @@@
        # with open(r"D:\vs code\python\FileFlow\testdoc\file_info_list.json", "w", encoding="utf-8") as f:
        #     json.dump(file_info_list, f, ensure_ascii=False, indent=2)

        # === 步骤2-3: 调用AI总结每个文件 ===
        print("\n开始步骤2-3: 调用AI总结每个文件...")
        classifier = FileClassifier(API_KEY)
        summarized_files = process_files_with_ai(file_info_list, classifier)

        if not summarized_files:
            print("警告: 没有成功总结任何文件")
            return False

        # === 步骤4-5: 调用AI分类文件 ===
        classified_files = classify_and_standardize(summarized_files, classifier)
        if not classified_files:
            return False

        # === 步骤7: 组织文件 ===
        try:
            organize_files(classified_files["files"])
        except Exception as e:
            print(f"组织文件时出错: {str(e)}")
            return False

        # === 步骤8: 补全分类信息 ===
        if not complete_category_info(classified_files):
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