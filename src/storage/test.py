import os
from database_build import * 
import database
def get_connection():
    return sqlite3.connect("fileflow_database.db")  # 这里就是连接的数据库文件
# 测试数据
test_folders = [
    {
        "name": "docs",
        "absolute_path": "/project/docs",
        "ai_description": "项目文档文件夹",
        "size": 4096,
        "created_time": "2025-06-01 10:00:00"
    },
    {
        "name": "images",
        "absolute_path": "/project/images",
        "ai_description": "图片资源文件夹",
        "size": 8192,
        "created_time": "2025-06-01 10:05:00"
    }
]

test_files = [
    {
        "name": "readme.txt",
        "absolute_path": "/project/docs/readme.txt",
        "extension": "txt",
        "size": 1024,
        "ai_description": "项目说明文档",
        "created_time": "2025-06-01 10:10:00",
        "content":"这是内容",
        "short_content":"这是总结"
    },
    {
        "name": "logo.png",
        "absolute_path": "/project/images/logo.png",
        "extension": "png",
        "size": 204800,
        "ai_description": "公司LOGO图片",
        "created_time": "2025-06-01 10:15:00",
        "content":"这是内容",
        "short_content":"这是总结"
    }
]

# 测试文件操作
print(""" \n****************************fileAdd模块************************ \n""")
for f in test_files:
    database.fileAdd(f)
print(""" \n****************************fileshow模块************************ \n""")
files=database.fileShow()
for f in files:
    print(f)
print(""" \n****************************filesearch模块************************ \n""")
file=database.fileSearchByName("logo.png") 
print(file)
file=database.fileSearchByPath("/project/docs/readme.txt") 
print(file)
print(""" \n****************************filedelete模块************************ \n""")
file="logo.png"
database.fileDeleteByName(file)
file="/project/docs/readme.txt"
database.fileDeleteByPath(file)



# 测试目录操作
print(""" \n****************************foldadd模块************************ \n""")
for f in test_folders:
    database.folderAdd(f)
print(""" \n****************************foldshow模块************************ \n""")
folders=database.folderShow()
for f in folders:
    print(f)
print(""" \n****************************folddelete模块************************ \n""")
database.folderDeleteByName("docs")
database.folderDeleteByPath("/project/images")

database.reset_database()