import os
import sqlite3
import pandas as pd
from docx import Document
import pdfplumber  # Changed from PyPDF2 to pdfplumber
from datetime import datetime

def parse_file(file_path):
    """解析单个文件的核心函数"""
    file_info = {
        "name": os.path.basename(file_path),
        "absolute_path": os.path.abspath(file_path),
        "extension": os.path.splitext(file_path)[1].lower(),
        "created_time": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
        "size_bytes": os.path.getsize(file_path),
        "content": ""
    }

    try:
        # PDF文件处理 (using pdfplumber now)
        if file_info["extension"] == '.pdf':
            with pdfplumber.open(file_path) as pdf:
                file_info["content"] = "\n".join([page.extract_text() for page in pdf.pages])
        
        # Excel文件处理
        elif file_info["extension"] in ('.xlsx', '.xls'):
            df = pd.read_excel(file_path)
            file_info["content"] = df.to_string()
        
        # Word文件处理
        elif file_info["extension"] == '.docx':
            doc = Document(file_path)
            file_info["content"] = "\n".join([para.text for para in doc.paragraphs])
        
        # 文本文件处理
        elif file_info["extension"] == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                file_info["content"] = f.read()
        
        else:
            file_info["content"] = "<不支持的文件格式>"
    
    except Exception as e:
        file_info["content"] = f"<读取错误: {str(e)}>"
    
    return file_info

def parse_folder(directory):
    """处理目录中的所有文件（与数据库交互前）"""
    return [parse_file(os.path.join(directory, f)) 
            for f in os.listdir(directory) 
            if os.path.isfile(os.path.join(directory, f))]


def save_to_db(file_data, db_path='file_database.db'):
    """将解析结果存入数据库（对应架构图中间模块）"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 创建表（如果不存在）
    c.execute('''CREATE TABLE IF NOT EXISTS files
                 (name TEXT, path TEXT PRIMARY KEY, extension TEXT, 
                  created_time TEXT, size INTEGER, content TEXT)''')
    
    # 插入或更新数据
    for item in file_data:
        c.execute('''INSERT OR REPLACE INTO files VALUES 
                     (?, ?, ?, ?, ?, ?)''', 
                     (item['name'], item['absolute_path'], item['extension'],
                      item['created_time'], item['size_bytes'], item['content']))
    
    conn.commit()
    conn.close()

def get_directories(db_path='file_database.db'):
    """从数据库获取目录信息（对应架构图功能2）"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT DISTINCT 
                 substr(path, 1, length(path)-length(name)) as directory_path,
                 substr(path, 1, length(path)-length(name)) as directory_description
                 FROM files''')
    return [{"path": row[0], "description": row[1]} for row in c.fetchall()]