import os
from typing import List, Dict, Optional

class FileSearcher:
    """文件搜索模块"""
    
    @staticmethod
    def get_search_target_files(search_path: str) -> List[Dict[str, Optional[str]]]:
        """
        核心搜索功能
        
        参数:
            search_path: 要搜索的目录路径
        
        返回:
            字典列表:
                [{
                    "文件路径": "/path/to/file.txt",    # 对应图片左侧下方框第一项
                    "文件名字": "file.txt",            # 对应"名字"
                    "文件类型": ".txt",                # 对应"类型"
                    "文件大小": "1024",               # 对应"大小"（字符串形式）
                    "一句话描述": "示例文本文件"        # 对应图片最下方字段
                }]
        """
        results = []
        
        try:
            # 遍历目录
            for root, _, files in os.walk(search_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    
                    # 获取文件信息
                    file_info = {
                        "文件路径": filepath,
                        "文件名字": filename,
                        "文件类型": os.path.splitext(filename)[1],  # 提取扩展名
                        "文件大小": str(os.path.getsize(filepath)),  # 转为字符串
                        "一句话描述": ""  # 预留描述字段
                    }
                    results.append(file_info)
            
        except Exception as e:
            print(f"[搜索失败] 错误: {type(e).__name__} - {str(e)}")
        
        return results