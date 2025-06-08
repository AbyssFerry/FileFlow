from typing import Dict, Any
import sqlite3

def merge_file_info(info1, info2):
    """
    合并两个文件信息字典并去除重复字段
    参数:
        info1: 第一个文件信息字典
        info2: 第二个文件信息字典
    返回:
        合并并去重后的新字典
    """
    merged_info = {}
    
    # 合并第一个字典
    for key, value in info1.items():
        if key not in merged_info:  # 如果键不存在则添加
            merged_info[key] = value
    
    # 合并第二个字典，跳过已存在的键
    for key, value in info2.items():
        if key not in merged_info:  # 只添加不重复的键
            merged_info[key] = value
        # 特殊处理created_time这种完全重复的字段
        elif key == "created_time" and value == info1.get(key):
            continue  # 完全相同的created_time则跳过
    
    return merged_info

