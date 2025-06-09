import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from src.storage.database import fileAdd

def pack_init_file(fileNewPath):
    # 转换字典结构
    packed_file = {
        "name": fileNewPath["name"],
        "absolute_path": fileNewPath["new_absolute_path"],  # 使用原本的new_absolute_path
        "extension": fileNewPath["extension"],
        "created_time": fileNewPath["created_time"],
        "size": fileNewPath["size"],
        "ai_description": fileNewPath["ai_description"],
        "content": fileNewPath["content"],
        "short_content": fileNewPath["short_content"]
    }
    
    # 调用数据库的fileAdd方法
    fileAdd(packed_file)
    
    # 返回成功
    return {"status": "success"}