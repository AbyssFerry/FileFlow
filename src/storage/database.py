
import sqlite3

DB_NAME = 'fileflow_database.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def insert_file(name, path, extension='none', size=0, content='', short_content=''):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM file WHERE absolute_path = ?', (path,))
            if cursor.fetchone():
                return False, "路径已存在，插入跳过"

            cursor.execute('''
                INSERT INTO file (name, absolute_path, extension, size, content, short_content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, path, extension, size, content, short_content))
            conn.commit()
            return True, "插入成功"
    except sqlite3.IntegrityError as e:
        return False, f"约束错误：{e}"
    except Exception as e:
        return False, f"未知错误：{e}"

def query_files():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM file')
        return cursor.fetchall()

def update_file_size(name, new_size):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE file
            SET size = ?, modified_time = datetime('now', 'localtime')
            WHERE name = ?
        ''', (new_size, name))
        conn.commit()

def update_file_short_content(name, new_short_content):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE file
                SET short_content = ?, modified_time = datetime('now', 'localtime')
                WHERE name = ?
            ''', (new_short_content, name))
            if cursor.rowcount == 0:
                return False, f"文件名 '{name}' 未找到，更新失败"
            conn.commit()
            return True, "文件分析内容更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"
    
def delete_file(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM file WHERE name = ?', (name,))
        conn.commit()

def update_file_content(name, new_content):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE file
                SET content = ?, modified_time = datetime('now', 'localtime')
                WHERE name = ?
            ''', (new_content, name))

            if cursor.rowcount == 0:
                return False, f"文件名 '{name}' 未找到，更新失败"

            conn.commit()
            return True, "文件内容更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"
    

def update_file_ai_description(name, new_description):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE file
                SET ai_description = ?, modified_time = datetime('now', 'localtime')
                WHERE name = ?
            ''', (new_description, name))

            if cursor.rowcount == 0:
                return False, f"文件名 '{name}' 未找到，更新失败"

            conn.commit()
            return True, "AI 描述更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"
    

# ===============================
#          目录表操作函数
# ===============================

def insert_directory(name, absolute_path, size=0, ai_description='待分析'):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM directory WHERE absolute_path = ?', (absolute_path,))
            if cursor.fetchone():
                return False, "路径已存在，插入跳过"

            cursor.execute('''
                INSERT INTO directory (name, absolute_path, size, ai_description)
                VALUES (?, ?, ?, ?)
            ''', (name, absolute_path, size, ai_description))
            conn.commit()
            return True, "插入成功"
    except sqlite3.IntegrityError as e:
        return False, f"约束错误：{e}"
    except Exception as e:
        return False, f"未知错误：{e}"

def query_directories():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM directory')
        return cursor.fetchall()

def update_directory_description(path, new_description):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE directory
            SET ai_description = ?
            WHERE absolute_path = ?
        ''', (new_description, path))
        conn.commit()

def delete_directory_by_path(path):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM directory WHERE absolute_path = ?', (path,))
        conn.commit()

def update_directory_description(name, new_description):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE directory
                SET ai_description = ?, register_time = datetime('now', 'localtime')
                WHERE name = ?
            ''', (new_description, name))
            if cursor.rowcount == 0:
                return False, f"目录名 '{name}' 未找到，更新失败"
            conn.commit()
            return True, "目录分析描述更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"

def update_directory_size(name, new_size):
    try:
        if new_size < 0:
            return False, "大小不能为负数"

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE directory
                SET size = ?, register_time = datetime('now', 'localtime')
                WHERE name = ?
            ''', (new_size, name))

            if cursor.rowcount == 0:
                return False, f"目录名 '{name}' 未找到，更新失败"

            conn.commit()
            return True, "目录大小更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"

