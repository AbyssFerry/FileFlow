import sqlite3  # 或其他数据库驱动
from typing import Dict, List, Union

class DatabasePacker:
    """处理文件和目录数据存储的模块"""
    
    @staticmethod
    def pack_init_datas(
        db_connection: sqlite3.Connection,
        data: Dict[str, Union[str, List[Dict]]]
    ) -> bool:
        """
        核心数据打包功能
        
        参数:
            db_connection: 已建立的数据库连接
            data: 包含两种数据格式的字典:
                - 文件数据: {
                    "type": "file",
                    "name": "example.pdf",
                    "old_path": "/old/path/example.pdf",
                    "new_path": "/new/path/example.pdf",
                    "ai_summary": "AI生成的内容总结",
                    "description": "一句话描述"
                  }
                - 目录数据: {
                    "type": "directory",
                    "path": "/target/directory",
                    "files": [文件数据1, 文件数据2...]
                  }
        
        返回:
            bool: 操作是否成功
        """
        try:
            cursor = db_connection.cursor()
            
            # 创建表结构
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS directories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    old_path TEXT,
                    new_path TEXT,
                    ai_summary TEXT,
                    description TEXT,
                    directory_id INTEGER,
                    FOREIGN KEY(directory_id) REFERENCES directories(id)
                )
            """)
            
            # 处理目录数据
            if data.get("type") == "directory":
                # 插入目录记录
                cursor.execute(
                    "INSERT OR IGNORE INTO directories (path) VALUES (?)",
                    (data["path"],)
                )
                
                # 获取目录ID
                cursor.execute(
                    "SELECT id FROM directories WHERE path = ?",
                    (data["path"],)
                )
                dir_id = cursor.fetchone()[0]
                
                # 处理目录下的文件
                for file_data in data.get("files", []):
                    cursor.execute(
                        """INSERT INTO files 
                        (name, old_path, new_path, ai_summary, description, directory_id)
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        (
                            file_data["name"],
                            file_data["old_path"],
                            file_data["new_path"],
                            file_data.get("ai_summary"),
                            file_data.get("description"),
                            dir_id
                        )
                    )
            
            # 处理独立文件数据
            elif data.get("type") == "file":
                cursor.execute(
                    """INSERT INTO files 
                    (name, old_path, new_path, ai_summary, description)
                    VALUES (?, ?, ?, ?, ?)""",
                    (
                        data["name"],
                        data["old_path"],
                        data["new_path"],
                        data.get("ai_summary"),
                        data.get("description")
                    )
                )
            
            db_connection.commit()
            return True
            
        except Exception as e:
            db_connection.rollback()
            print(f"[数据打包失败] 错误: {str(e)}")
            return False