import os
import sqlite3
from datetime import datetime

"""parse_folder_path模块"""

def parse_folder_path(directory):
    file_info_list = []

    #遍历目录中的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        #跳过子目录
        if os.path.isfile(file_path):
            # 获取文件信息
            file_info = {
                "name": filename,  #文件名
                "absolute_path": os.path.abspath(file_path),  #绝对路径
                "extension": os.path.splitext(filename)[1],  #扩展名
                "created_time": datetime.fromtimestamp(  #创建时间
                    os.path.getctime(file_path)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "size_bytes": os.path.getsize(file_path),  #文件大小
                "content": ""  # 文件内容占位
            }
            # 读取文件内容
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_info["content"] = f.read()
            except UnicodeDecodeError:
                file_info["content"] = "<二进制文件，内容未显示>"
            file_info_list.append(file_info)
    return file_info_list