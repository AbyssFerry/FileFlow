import sqlite3
def get_connection():
    return sqlite3.connect("fileflow_database.db")  # 这里就是连接的数据库文件

""" ****************************fileAdd模块************************ """
def fileAdd(file_data: dict):
    sql = '''
    INSERT INTO file (name, absolute_path, extension, created_time, size, ai_description, content, short_content)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    values = (
        file_data["name"],
        file_data["absolute_path"],
        file_data["extension"],
        file_data["created_time"],
        file_data["size"],
        file_data["ai_description"],
        file_data["content"],    
        file_data["short_content"]
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            print("[添加成功] 文件信息如下：")
            for k, v in file_data.items():
                print(f"  {k}: {v}")
        except sqlite3.IntegrityError as e:
            print(f"[添加失败] 文件路径已存在：{file_data['absolute_path']}")
            print(f"错误信息: {e}")





""" ****************************fileShow模块************************ """
def fileShow():
    sql = "SELECT * FROM file"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in rows]



""" ****************************fileDelete模块************************ """
def fileDeleteByName(name: str):
    sql = "DELETE FROM file WHERE name = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (name.strip(),))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[删除成功] 已删除所有文件名为 '{name}' 的文件（共 {cursor.rowcount} 条）")
        else:
            print(f"[未找到] 没有找到文件名为 '{name}' 的文件")

def fileDeleteByPath(path: str):
    sql = "DELETE FROM file WHERE absolute_path = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (path.strip(),))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[删除成功] 已删除文件，路径: {path}")
        else:
            print(f"[未找到] 没有找到路径为 {path} 的文件")




""" ****************************fileSearch模块************************ """
def fileSearchByName(name: str):
    sql = "SELECT * FROM file WHERE name = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (name.strip(),))
        row = cursor.fetchone()
        if row:
            col_names = [desc[0] for desc in cursor.description]
            return dict(zip(col_names, row))
        return None
    
def fileSearchByPath(path: str):
    sql = "SELECT * FROM file WHERE absolute_path = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (path.strip(),))
        row = cursor.fetchone()
        if row:
            col_names = [desc[0] for desc in cursor.description]
            return dict(zip(col_names, row))
        return None




""" ****************************folderAdd模块************************ """
def folderAdd(folder_data: dict):
    sql = '''
    INSERT INTO directory (name, absolute_path, created_time, size, ai_description)
    VALUES (?, ?, ?, ?, ?)
    '''
    values = (
        folder_data["name"],
        folder_data["absolute_path"],
        folder_data["created_time"],
        folder_data["size"],
        folder_data["ai_description"]
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            print("[添加成功] 目录信息如下：")
            for k, v in folder_data.items():
                print(f"  {k}: {v}")
        except sqlite3.IntegrityError as e:
            print(f"[添加失败] 目录路径已存在：{folder_data['absolute_path']}")
            print(f"错误信息: {e}")



""" ****************************folderDelete模块************************ """
def folderDeleteByPath(path: str):
    sql = "DELETE FROM directory WHERE absolute_path = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (path.strip(),))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[删除成功] 已删除目录，路径: {path}")
        else:
            print(f"[未找到] 没有找到路径为 {path} 的目录")

def folderDeleteByName(name: str):
    sql = "DELETE FROM directory WHERE name = ?"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (name.strip(),))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"[删除成功] 已删除所有名称为 '{name}' 的目录（共 {cursor.rowcount} 条）")
        else:
            print(f"[未找到] 没有找到名称为 '{name}' 的目录")


""" ****************************folderShow模块************************ """

def folderShow():
    sql = "SELECT * FROM directory"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in rows]

def reset_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM file")
        cursor.execute("DELETE FROM directory")
        conn.commit()
        print("✅ 数据库内容已初始化（文件表和目录表数据已清空）")