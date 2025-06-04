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
""" ****************************fileAdd模块************************ """
a=database.fileAdd(test_files)
print(a)
""" ****************************fileShow模块************************ """
database.fileShow()
""" ****************************fileSearch模块************************ """
database.fileSearch("/project/images/logo.png")
""" ****************************fileDelete模块************************ """
database.fileDelete()
# 测试目录操作
""" ****************************folderAdd模块************************ """
b=database.folderAdd(test_folders)
print(b)
""" ****************************folderShow模块************************ """
database.folderShow()
""" ****************************folderDelete模块************************ """
database.folderDelete()

""" ****************************初始化************************ """

database.reset_database()