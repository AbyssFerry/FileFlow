import os
import sys
from src.ui.uiprint import print
# 获取项目根路径并统一使用正斜杠
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.storage.database import fileSearchByPath

def get_search_target_files(match_files):
    files = []
    
    for match_file in match_files:
        # 确保路径格式统一为SQL风格
        absolute_path = match_file["absolute_path"].replace('\\', '/')
        
        # 调用数据库查询文件信息
        file = fileSearchByPath(absolute_path)
        
        # 转换为前端需要的格式（确保路径统一）
        fileForUI = {
            "file_path": file["absolute_path"].replace('\\', '/'),  # 统一路径格式
            "file_name": file["name"],
            "file_type": file["extension"],
            "file_size": file["size"],
            "short_description": file["short_content"]
        }
        
        files.append(fileForUI)
    
    return files