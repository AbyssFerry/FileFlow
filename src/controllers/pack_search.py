import os
import sqlite3
from datetime import datetime

def pack(user_input: str, db_items: list) -> dict:
    """
    打包功能
    参数:
        user_input: 用户输入字符串
        db_items: 数据库中的文件和目录列表
    返回:
        结构:
        {
            "query_statement": 打包后的查询语句,
            "file_statements": 文件信息列表,
            "dir_statements": 目录信息列表
        }
    """
    # 模块核心处理逻辑
    query = f"QUERY: {user_input.upper()}"  # 示例查询语句生成

    # 分离文件和目录
    files = []
    dirs = []
    for item in db_items:
        target = files if item.get('type') == 'file' else dirs
        target.append({
            'name': item['name'],
            'description': item.get('description', ''),
            'path': item['path']
        })

    return {
        "query_statement": query,
        "file_statements": [
            f"FILE: {f['name']} | DESC: {f['description']} | PATH: {f['path']}"
            for f in files
        ],
        "dir_statements": [
            f"DIR: {d['name']} | DESC: {d['description']} | PATH: {d['path']}"
            for d in dirs
        ]
    }