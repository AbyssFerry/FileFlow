import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.storage.database import fileSearchByPath
def get_search_target_files(match_files):
    files = []
    
    for match_file in match_files:
        # 调用数据库查询文件信息
        file = fileSearchByPath(match_file["absolute_path"])
        
        # 转换为前端需要的格式
        fileForUI = {
            "file_path": file["absolute_path"],
            "file_name": file["name"],
            "file_type": file["extension"],
            "file_size": file["size"],
            "short_description": file["short_content"]
        }
        
        files.append(fileForUI)
    
    return files