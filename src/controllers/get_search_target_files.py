import os
from typing import List, Dict, Optional

class FileSearcher:
    """文件搜索匹配模块（通过小列表路径匹配大列表中的文件信息）"""
    
    @staticmethod
    def find_matching_files(large_list: List[Dict[str, str]], 
                           small_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        通过小列表中的路径信息在大列表中查找匹配的文件信息
        
        参数:
            large_list: 包含完整文件信息的大列表
            small_list: 只包含路径信息的小列表
        
        返回:
            字典列表（包含五个字段）:
                [{
                    "name": "file.txt",            # 文件名
                    "absolute_path": "/path/to/file.txt",    # 完整路径
                    "extension": ".txt",                # 扩展名
                    "size": "1024",               # 大小（字符串）
                    "ai_description": "示例描述"            # 描述内容
                }]
        """
        results = []
        
        # 从小列表中提取所有需要匹配的路径
        target_paths = {item.get("path", item.get("absolute_path", "")).lower() 
                       for item in small_list if "path" in item or "absolute_path" in item}
        
        # 在大列表中查找匹配项
        for file_info in large_list:
            if file_info.get("absolute_path", "").lower() in target_paths:
                # 确保返回的字典包含所有五个字段
                matched_file = {
                    "name": file_info.get("name", ""),
                    "absolute_path": file_info.get("absolute_path", ""),
                    "extension": file_info.get("extension", ""),
                    "size": str(file_info.get("size", "0")),
                    "ai_description": file_info.get("ai_description", "无描述")
                }
                results.append(matched_file)
        
        return results