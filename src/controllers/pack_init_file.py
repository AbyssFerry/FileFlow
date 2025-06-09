import os
import sys

# 获取项目根路径并统一使用正斜杠
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.storage.database import fileAdd

def pack_init_file(fileNewPath):
    # 标准化路径为SQL风格(正斜杠)
    new_absolute_path = fileNewPath["new_absolute_path"].replace('\\', '/')
    
    # 转换字典结构（确保路径统一格式）
    packed_file = {
        "name": fileNewPath["name"],
        "absolute_path": new_absolute_path,  # 使用标准化后的路径
        "extension": fileNewPath["extension"],
        "created_time": fileNewPath["created_time"],
        "size": fileNewPath["size"],
        "ai_description": fileNewPath["ai_description"],
        "content": fileNewPath["content"],
        "short_content": fileNewPath["short_content"]
    }
    
    try:
        # 调用数据库的fileAdd方法
        fileAdd(packed_file)
        """print("-"*20)   # @@@@@
        print("模块2")
        print(packed_file)  # @@@@@
        print("-"*20)   # @@@@@"""
        return {
            "status": "success",
            "message": f"文件已成功添加到数据库: {new_absolute_path}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"无法添加文件到数据库: {str(e)}",
            "file_path": new_absolute_path  # 返回标准化路径用于调试
        }