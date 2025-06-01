# ===============================
#          文件表操作函数
# ===============================

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
    
def delete_file(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM file WHERE name = ?', (name,))
        conn.commit()

def update_file_fields_by_path(path, fields):
    try:
        if not fields:
            return False, "没有需要更新的字段"
        assignments = ", ".join([f"{k} = ?" for k in fields])
        sql = f'''
            UPDATE file
            SET {assignments}, modified_time = datetime('now', 'localtime')
            WHERE absolute_path = ?
        '''
        values = list(fields.values())
        values.append(path)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                return False, f"文件路径 '{path}' 未找到，更新失败"
            conn.commit()
            return True, "文件信息更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"
    
# ===== 单字段更新封装（文件） =====
def update_file_ai_description_by_path(path, description):
    return update_file_fields_by_path(path, {"ai_description": description})

def update_file_content_by_path(path, content):
    return update_file_fields_by_path(path, {"content": content})

def update_file_short_content_by_path(path, short):
    return update_file_fields_by_path(path, {"short_content": short})



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


def delete_directory_by_path(path):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM directory WHERE absolute_path = ?', (path,))
        conn.commit()

def update_directory_fields_by_path(path, fields):
    try:
        if not fields:
            return False, "没有需要更新的字段"
        assignments = ", ".join([f"{k} = ?" for k in fields])
        sql = f'''
            UPDATE directory
            SET {assignments}, register_time = datetime('now', 'localtime')
            WHERE absolute_path = ?
        '''
        values = list(fields.values())
        values.append(path)

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                return False, f"目录路径 '{path}' 未找到，更新失败"
            conn.commit()
            return True, "目录信息更新成功"
    except Exception as e:
        return False, f"更新失败：{e}"

# ===== 单字段更新封装（目录） =====
def update_directory_ai_description_by_path(path, description):
    return update_directory_fields_by_path(path, {"ai_description": description})

def update_directory_size_by_path(path, size):
    return update_directory_fields_by_path(path, {"size": size})