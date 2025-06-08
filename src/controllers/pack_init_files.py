from typing import Dict, Any
import sqlite3
from datetime import datetime

def merge_file_info(info1: Dict[str, Any], info2: Dict[str, Any], db_path: str = 'file_database.db') -> Dict[str, Any]:
    """
    合并两个文件信息字典并去除重复字段，然后将结果存入数据库
    
    参数:
        info1: 第一个文件信息字典
        info2: 第二个文件信息字典
        db_path: 数据库文件路径(可选)
    
    返回:
        合并并去重后的新字典
    """
    # 合并字典
    merged_info = {}
    
    # 合并第一个字典
    for key, value in info1.items():
        if key not in merged_info:
            merged_info[key] = value
    
    # 合并第二个字典，跳过已存在的键
    for key, value in info2.items():
        if key not in merged_info:
            merged_info[key] = value
        elif key == "created_time" and value == info1.get(key):
            continue
    
    # 存入数据库
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 创建表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS merged_file_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            absolute_path TEXT UNIQUE NOT NULL,
            extension TEXT,
            created_time TEXT,
            size INTEGER,
            description TEXT,
            short_content TEXT,
            content TEXT,
            merge_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 准备数据（修正字段名并添加合并时间）
        db_data = {
            'name': merged_info.get('name'),
            'absolute_path': merged_info.get('absolut_path'),  # 修正拼写错误
            'extension': merged_info.get('extension'),
            'created_time': merged_info.get('created_time'),
            'size': int(merged_info.get('size', 0)) if merged_info.get('size') else 0,
            'description': merged_info.get('description'),
            'short_content': merged_info.get('short_content'),
            'content': merged_info.get('content'),
            'merge_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 使用UPSERT语法插入或更新数据
        cursor.execute('''
        INSERT INTO merged_file_info (
            name, absolute_path, extension, created_time, size,
            description, short_content, content, merge_time
        ) VALUES (
            :name, :absolute_path, :extension, :created_time, :size,
            :description, :short_content, :content, :merge_time
        )
        ON CONFLICT(absolute_path) DO UPDATE SET
            name = excluded.name,
            extension = excluded.extension,
            created_time = excluded.created_time,
            size = excluded.size,
            description = excluded.description,
            short_content = excluded.short_content,
            content = excluded.content,
            merge_time = excluded.merge_time
        ''', db_data)
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"数据库操作失败: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
    return merged_info