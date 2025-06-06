import sqlite3
from typing import Dict, List, Union, Optional


class DatabasePacker:
    """处理文件和目录数据存储的模块（基于已有数据库）"""

    @staticmethod
    def pack_init_datas(
            db_path: str,
            data: Dict[str, Union[str, List[Dict]]]
    ) -> bool:
        """
        核心数据打包功能（使用已有数据库）

        参数:
            db_path: 已有数据库文件路径
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
        conn = None
        try:
            # 连接到已有数据库
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # 检查表是否存在（兼容性处理）
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='directories'
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE directories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        path TEXT UNIQUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='files'
            """)
            if not cursor.fetchone():
                cursor.execute("""
                    CREATE TABLE files (
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

            # 处理数据插入
            if data.get("type") == "directory":
                # 插入或获取目录ID
                dir_id = DatabasePacker._get_or_create_directory(
                    cursor, data["path"]
                )

                # 批量插入文件
                file_records = [
                    (
                        f["name"],
                        f["old_path"],
                        f["new_path"],
                        f.get("ai_summary"),
                        f.get("description"),
                        dir_id
                    )
                    for f in data.get("files", [])
                ]

                cursor.executemany(
                    """INSERT INTO files 
                    (name, old_path, new_path, ai_summary, description, directory_id)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    file_records
                )

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

            conn.commit()
            return True

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"[数据库操作失败] 错误: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def _get_or_create_directory(
            cursor: sqlite3.Cursor,
            path: str
    ) -> Optional[int]:
        """获取或创建目录记录"""
        cursor.execute(
            "SELECT id FROM directories WHERE path = ?",
            (path,)
        )
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            cursor.execute(
                "INSERT INTO directories (path) VALUES (?)",
                (path,)
            )
            return cursor.lastrowid