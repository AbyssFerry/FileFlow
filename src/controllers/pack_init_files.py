import sys
from pathlib import Path
import sqlite3
from src.ui.uiprint import print

# 添加项目根目录到Python路径 (使用Path对象自动处理路径分隔符)
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# 现在可以使用绝对导入
from src.storage.database import folderAdd, fileAdd
from src.storage.database_build import create_database

def pack_init_files(classified_files):
    """
    处理classified_files数据并调用数据库添加文件和文件夹
    所有路径存储使用SQL风格的正斜杠(/)
    
    Args:
        classified_files (dict): 包含文件和分类信息的字典
            {
                "files": [...],  # 文件列表
                "categories": [...]  # 分类列表
            }
    
    Returns:
        str: "成功"
    """
    # 处理files数据并调用fileAdd
    for file_info in classified_files["files"]:
        # 标准化路径为SQL风格
        abs_path = file_info["new_absolute_path"].replace('\\', '/')
        
        # 构建file数据结构
        file_data = {
            "name": file_info["name"],
            "absolute_path": abs_path,  # 使用标准化路径
            "extension": file_info["extension"],
            "created_time": file_info["created_time"],
            "size": file_info["size"],
            "ai_description": file_info["ai_description"],
            "content": file_info["content"],  # 保留但不使用
            "short_content": file_info["short_content"]  # 保留但不使用
        }
        """print("-"*20)   # @@@@@
        print("模块1：file_date") # @@@@@
        print(file_data)  # @@@@@
        print("-"*20)   # @@@@@"""
        fileAdd(file_data)
    
    # 处理categories数据并调用folderAdd
    for category_info in classified_files["categories"]:
        # 标准化路径为SQL风格
        abs_path = category_info["absolute_path"].replace('\\', '/')
        
        # 构建folder数据结构
        folder_data = {
            "name": category_info["name"],
            "absolute_path": abs_path,  # 使用标准化路径
            "created_time": category_info["created_time"],
            "size": category_info["size"],
            "ai_description": category_info["ai_description"]
        }
        folderAdd(folder_data)
        """print("-"*20)   # @@@@@
        print("模块1：folder_data") # @@@@@
        print(folder_data)  # @@@@@
        print("-"*20)   # @@@@@"""

    return "成功"