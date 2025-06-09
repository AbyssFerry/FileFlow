import sqlite3

def create_database():
    # 创建数据库连接
    conn = sqlite3.connect('fileflow_database.db')
    cursor = conn.cursor()

    # 创建目录表（directory）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS directory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT CHECK(LENGTH(name) > 0),
        absolute_path TEXT UNIQUE NOT NULL,
        created_time TEXT DEFAULT (datetime('now', 'localtime')),
        register_time TEXT DEFAULT (datetime('now', 'localtime')),
        size INTEGER DEFAULT 0 CHECK(size >= 0),
        ai_description TEXT DEFAULT '待分析'
    )
    ''')

    # 创建文件表（file）
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT CHECK(LENGTH(name) > 0),
        absolute_path TEXT UNIQUE NOT NULL,
        extension TEXT DEFAULT 'none',
        created_time TEXT DEFAULT (datetime('now', 'localtime')),
        modified_time TEXT DEFAULT (datetime('now', 'localtime')),
        size INTEGER DEFAULT 0 CHECK(size >= 0),
        ai_description TEXT DEFAULT '待分析',
        content TEXT,
        short_content TEXT
    )
    ''')

    # 提交更改并关闭连接
    conn.commit()
    conn.close()