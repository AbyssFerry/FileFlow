from typing import Dict, Any
import sqlite3

class DataPacker:
    """元数据打包模块"""
    
    @staticmethod
    def pack_init_datas(
        db_conn: sqlite3.Connection,
        file_meta: Dict[str, Any]
    ) -> bool:
        """
        核心打包逻辑（
        
        参数:
            db_conn: 数据库连接对象
            file_meta: 必须包含图片中左侧框所有字段:
                {
                    "文件名": "example.txt",
                    "文件新路径": "/new/path/example.txt",
                    "文件旧路径": "/old/path/example.txt",
                    "文件总结内容": "AI生成的内容摘要",
                    "文件一句话描述": "这是一个示例文件",
                    "目录描述内容": "存放文档的目录",
                    "移动理由": "整理归档"
                }
        
        返回:
            bool: 数据是否成功写入数据库
        """
        try:
            # 验证必须字段
            required_fields = [
                "文件名", "文件新路径", "文件旧路径",
                "文件总结内容", "文件一句话描述",
                "目录描述内容", "移动理由"
            ]
            if not all(field in file_meta for field in required_fields):
                missing = [f for f in required_fields if f not in file_meta]
                raise ValueError(f"缺少必要字段: {missing}")

            # 创建数据库表
            cursor = db_conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS file_metadata (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    new_path TEXT NOT NULL,
                    old_path TEXT NOT NULL,
                    ai_summary TEXT,
                    description TEXT,
                    dir_description TEXT,
                    move_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 插入数据
            cursor.execute("""
                INSERT INTO file_metadata (
                    filename, new_path, old_path,
                    ai_summary, description,
                    dir_description, move_reason
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                file_meta["文件名"],
                file_meta["文件新路径"],
                file_meta["文件旧路径"],
                file_meta["文件总结内容"],
                file_meta["文件一句话描述"],
                file_meta["目录描述内容"],
                file_meta["移动理由"]
            ))

            db_conn.commit()
            return True

        except Exception as e:
            db_conn.rollback()
            print(f"[打包失败] 错误: {str(e)}")
            return False