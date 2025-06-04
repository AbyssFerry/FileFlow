import sqlite3
def get_connection():
    return sqlite3.connect("fileflow_database.db")  # 这里就是连接的数据库文件

""" ****************************fileAdd模块************************ """
def fileAdd(data_list):
    print("***********调用了fileAdd模块************\n")
    """
    批量插入文件记录，create_time 由用户提供。
    """
    sql = '''
    INSERT INTO file (name, absolute_path, extension, size, ai_description, content, short_content, created_time)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''

    success_count = 0
    fail_count = 0

    with get_connection() as conn:
        cursor = conn.cursor()
        for item in data_list:
            try:
                values = (
                    item["name"],
                    item["absolute_path"],
                    item["extension"],
                    item["size"],
                    item["ai_description"],
                    item["content"],
                    item["short_content"],
                    item["created_time"]
                )
                cursor.execute(sql, values)
                conn.commit()
                success_count += 1
                print(f"✅ 插入成功 - 文件路径: {item['absolute_path']}")
                for k, v in item.items():
                    print(f"  {k}: {v}")
                print("-" * 40)
            except KeyError as e:
                fail_count += 1
                print(f"❌ 插入失败（字段缺失）: {e}")
                print("-" * 40)
            except sqlite3.IntegrityError as e:
                fail_count += 1
                print(f"❌ 插入失败（唯一约束）: {item.get('absolute_path', '未知路径')}")
                print("🔍 错误信息：", e)
                print("-" * 40)
            except Exception as e:
                fail_count += 1
                print(f"❌ 插入失败（未知错误）: {e}")
                print("-" * 40)

    print(f"\n📊 执行完成：共 {len(data_list)} 条，成功 {success_count} 条，失败 {fail_count} 条")





""" ****************************fileShow模块************************ """
def fileShow():
    print("***********调用了fileShow模块************\n")
    """
    查询文件表中所有记录，返回列表并打印。
    :return: list[dict] 所有文件记录
    """
    sql = '''
    SELECT id, name, absolute_path, extension, size, ai_description, created_time
    FROM file
    '''

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        print("📄 所有文件记录：\n")
        data = []
        for row in rows:
            record = {
                "id": row[0],
                "name": row[1],
                "absolute_path": row[2],
                "extension": row[3],
                "size": row[4],
                "ai_description": row[5],
                "created_time": row[6]
            }
            data.append(record)

            # 控制台打印
            print(f"🆔 ID             : {record['id']}")
            print(f"📄 文件名         : {record['name']}")
            print(f"  路径           : {record['absolute_path']}")
            print(f"  扩展名         : {record['extension']}")
            print(f"  大小           : {record['size']} Bytes")
            print(f"  AI描述         : {record['ai_description']}")
            print(f"  创建时间       : {record['created_time']}")
            print("-" * 50)

        if not data:
            print("❌ 暂无文件记录。")
        return data
    




""" ****************************fileDelete模块************************ """
def fileDelete():
    print("***********调用了fileDelete模块************\n")
    """
    用户交互式输入要删除的文件id，依次执行删除并打印提示信息。
    """
    ids_input = input("📝 请输入要删除的文件ID（多个ID以空格分隔）：\n> ")
    try:
        ids = [int(i) for i in ids_input.strip().split()]
    except ValueError:
        print("❌ 输入格式错误，请仅输入数字 ID。")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        for file_id in ids:
            cursor.execute("SELECT name FROM file WHERE id = ?", (file_id,))
            row = cursor.fetchone()
            if row:
                cursor.execute("DELETE FROM file WHERE id = ?", (file_id,))
                print(f"✅ 文件 ID {file_id}（{row[0]}）删除成功")
            else:
                print(f"⚠️ 文件 ID {file_id} 未找到，跳过")
        conn.commit()
    print("🗑️ 删除操作完成。")





""" ****************************fileSearch模块************************ """
def fileSearch(path: str):
    print("***********调用了fileSearch模块************\n")
    """
    根据文件的绝对路径查询并输出文件的所有属性信息。
    :param path: str 类型，文件的绝对路径
    """
    path = path.strip()
    if not path:
        print("❌ 错误：路径不能为空。")
        return

    sql = '''
    SELECT * FROM file WHERE absolute_path = ?
    '''

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (path,))
        row = cursor.fetchone()

        if row:
            # 获取字段名
            col_names = [desc[0] for desc in cursor.description]
            print("🔍 查询结果：\n")
            for key, value in zip(col_names, row):
                print(f"{key:15} : {value}")
        else:
            print(f"❌ 未找到路径为 '{path}' 的文件记录。")




""" ****************************folderAdd模块************************ """
def folderAdd(data_list):
    print("***********调用了folderAdd模块************\n")
    """
    批量插入目录记录，create_time 由用户提供。
    """
    sql = '''
    INSERT INTO directory (name, absolute_path, ai_description, size, created_time)
    VALUES (?, ?, ?, ?, ?)
    '''

    success_count = 0
    fail_count = 0

    with get_connection() as conn:
        cursor = conn.cursor()
        for item in data_list:
            try:
                values = (
                    item["name"],
                    item["absolute_path"],
                    item["ai_description"],
                    item["size"],
                    item["created_time"]
                )
                cursor.execute(sql, values)
                conn.commit()
                success_count += 1
                print(f"✅ 插入成功 - 目录路径: {item['absolute_path']}")
                for k, v in item.items():
                    print(f"  {k}: {v}")
                print("-" * 40)
            except KeyError as e:
                fail_count += 1
                print(f"❌ 插入失败（字段缺失）: {e}")
                print("-" * 40)
            except sqlite3.IntegrityError as e:
                fail_count += 1
                print(f"❌ 插入失败（唯一约束）: {item.get('absolute_path', '未知路径')}")
                print("🔍 错误信息：", e)
                print("-" * 40)
            except Exception as e:
                fail_count += 1
                print(f"❌ 插入失败（未知错误）: {e}")
                print("-" * 40)

    print(f"\n📊 执行完成：共 {len(data_list)} 条，成功 {success_count} 条，失败 {fail_count} 条")






""" ****************************folderDelete模块************************ """
def folderDelete():
    print("***********调用了folderDelete模块************\n")
    """
    用户交互式输入要删除的目录id，依次执行删除并打印提示信息。
    """
    ids_input = input("📝 请输入要删除的目录ID（多个ID以空格分隔）：\n> ")
    try:
        ids = [int(i) for i in ids_input.strip().split()]
    except ValueError:
        print("❌ 输入格式错误，请仅输入数字 ID。")
        return

    with get_connection() as conn:
        cursor = conn.cursor()
        for dir_id in ids:
            cursor.execute("SELECT name FROM directory WHERE id = ?", (dir_id,))
            row = cursor.fetchone()
            if row:
                cursor.execute("DELETE FROM directory WHERE id = ?", (dir_id,))
                print(f"✅ 目录 ID {dir_id}（{row[0]}）删除成功")
            else:
                print(f"⚠️ 目录 ID {dir_id} 未找到，跳过")
        conn.commit()
    print("🗑️ 目录删除操作完成。")




""" ****************************folderShow模块************************ """

import sqlite3
def get_connection():
    return sqlite3.connect("fileflow_database.db")  # 这里就是连接的数据库文件

def folderShow():
    print("***********调用了folderShow模块************\n")
    """
    查询目录表中所有记录（包括id）.返回列表并打印。
    :return: list[dict] 所有目录记录
    """
    sql = '''
    SELECT id, name, absolute_path, ai_description, size, created_time,register_time
    FROM directory
    '''

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("📁 所有目录记录：\n")
        data = []
        for row in rows:
            record = {
                "id": row[0],
                "name": row[1],
                "absolute_path": row[2],
                "size": row[4],
                "created_time": row[5],
                "ai_description": row[3],
                "register_time": row[6],
            }
            data.append(record)

            # 控制台打印
            print(f"🆔 ID         : {record['id']}")
            print(f"✅ 目录名      : {record['name']}")
            print(f"  路径       : {record['absolute_path']}")
            print(f"  描述       : {record['ai_description']}")
            print(f"  大小       : {record['size']} Bytes")
            print(f"  创建时间   : {record['created_time']}")
            print(f"  注册时间   : {record['register_time']}")
            print("-" * 40)

        if not data:
            print("❌ 暂无目录记录。")
        return data
    

def reset_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM file")
        cursor.execute("DELETE FROM directory")
        conn.commit()
        print("✅ 数据库内容已初始化（文件表和目录表数据已清空）")