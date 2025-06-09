import sys
import os
from typing import List, Dict, Any
from get_search_target_files import get_search_target_files

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.controllers_for_ai.ai_processing import FileClassifier
from src.storage.database import fileShow

def pack_search(query: str) -> List[Dict[str, Any]]:
    """
    根据查询字符串搜索匹配的文件
    
    参数:
        query (str): 搜索查询字符串，例如"关于奖学金的文件"
        
    返回:
        List[Dict[str, Any]]: 匹配的文件列表，包含详细文件信息
    """
    # 1. 接收查询参数（通过函数形参query已接收）
    
    # 2. 调用数据库获取所有文件
    try:
        files = fileShow()  # 调用数据库函数
    except Exception as e:
        raise RuntimeError(f"数据库查询失败: {str(e)}")
        
    # 3. 调用AI分类器获取匹配文件
    try:
        classifier = FileClassifier()  # 实例化
        match_files = classifier.get_match_files(query, files)
    except Exception as e:
        raise RuntimeError(f"AI匹配过程出错: {str(e)}")
    
    # 5. 获取目标文件详细信息
    try:
        result_files = get_search_target_files(match_files)
    except Exception as e:
        raise RuntimeError(f"文件信息获取失败: {str(e)}")
    
    # 6. 返回最终结果
    return result_files