import os
import sqlite3
from datetime import datetime

def get_file_info(directory):
    """
    获取指定目录下所有文件的信息

    参数:
        directory: 要遍历的目录路径

    返回:
        包含文件信息的字典列表，每个字典包含:
        - name: 文件名
        - absolute_path: 文件绝对路径
        - extension: 文件扩展名
        - created_time: 文件创建时间
        - size_bytes: 文件大小(字节)
        - content: 文件内容

    异常:
        当目录不存在时返回空列表并打印错误信息
    """
    file_info_list = []
    try:
        # 检查目录是否存在
        if not os.path.exists(directory):
            raise FileNotFoundError(f"目录不存在: {directory}")
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"路径不是目录: {directory}")
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_info = {
                    "name": filename,
                    "absolute_path": os.path.abspath(file_path),
                    "extension": os.path.splitext(filename)[1],
                    "created_time": datetime.fromtimestamp(
                        os.path.getctime(file_path)
                    ).strftime("%Y-%m-%d %H:%M:%S"),
                    "size_bytes": os.path.getsize(file_path),
                    "content": ""
                }
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_info["content"] = f.read()
                except UnicodeDecodeError:
                    file_info["content"] = "<二进制文件，内容未显示>"
                except Exception as e:
                    file_info["content"] = f"<读取文件出错: {str(e)}>"
                file_info_list.append(file_info)
    except Exception as e:
        print(f"错误: {str(e)}")
        return []
    return file_info_list
    
def get_database_directories(db_path):
    """
    获取SQLite数据库中所有目录的信息

    参数:
        db_path: SQLite数据库文件路径

    返回:
        包含目录信息的字典列表，每个字典包含:
        - name: 目录名
        - description: 目录描述
        - path: 目录路径

    异常:
        当数据库文件不存在时返回空列表并打印错误信息
    """
    directories = []
    try:
        # 检查数据库文件是否存在
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"数据库文件不存在: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='directories'")
        if not cursor.fetchone():
            raise ValueError("数据库中不存在'directories'表")
        cursor.execute("SELECT name, description, path FROM directories")
        rows = cursor.fetchall()
        for row in rows:
            directory_info = {
                "name": row[0],
                "description": row[1],
                "path": row[2]
            }
            directories.append(directory_info)
    except Exception as e:
        print(f"数据库错误: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return directories