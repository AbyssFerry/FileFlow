from typing import Dict, Any
import sqlite3

def merge_file_info(info1: Dict[str, Any], info2: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并两个文件信息字典并去除重复字段，特别处理文件内容(content)和创建时间(created_time)
    
    参数:
        info1: 第一个文件信息字典，包含文件名、路径、扩展名、创建时间、大小等内容
        info2: 第二个文件信息字典，包含类似结构的信息
        
    返回:
        合并并去重后的新字典，优先保留更完整的信息
        
    示例:
        >>> file1 = {"name": "公示1", "content": "内容1", "created_time": "2023-11-20"}
        >>> file2 = {"name": "公示1", "content": "内容2", "size": "2048"}
        >>> merge_file_info(file1, file2)
        {"name": "公示1", "content": "内容1", "created_time": "2023-11-20", "size": "2048"}
    """
    merged_info = {}
    
    # 优先处理内容字段，保留更长的内容
    if "content" in info1 or "content" in info2:
        content1 = info1.get("content", "")
        content2 = info2.get("content", "")
        merged_info["content"] = content1 if len(content1) > len(content2) else content2
    
    # 合并其他字段，优先保留info1的值
    for key in set(info1.keys()).union(info2.keys()):
        if key == "content":
            continue  # 已经处理过
            
        if key in info1:
            merged_info[key] = info1[key]
        elif key in info2:
            merged_info[key] = info2[key]
    
    # 特殊处理short_content/short content字段
    if "short_content" in merged_info or "short content" in merged_info:
        short1 = merged_info.get("short_content") or merged_info.get("short content")
        merged_info.pop("short content", None)
        merged_info["short_content"] = short1
    
    return merged_info