import sys
import os
from typing import List, Dict, Any
from src.controllers.get_search_target_files import get_search_target_files
from src.ui.uiprint import print
# 标准化项目根路径为SQL风格
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.controllers_for_ai.ai_processing import FileClassifier
from src.storage.database import fileShow
from src.ui.uiprint import print
def pack_search(query: str, API_KEY: str = "") -> List[Dict[str, Any]]:
    """
    根据查询字符串搜索匹配的文件
    所有路径存储使用SQL风格的正斜杠(/)
    
    参数:
        query (str): 搜索查询字符串，例如"关于奖学金的文件"
        
    返回:
        List[Dict[str, Any]]: 匹配的文件列表，包含详细文件信息（路径为SQL风格）
    """
    # 1. 接收查询参数（通过函数形参query已接收）
    
    # 2. 调用数据库获取所有文件
    try:
        files = fileShow()  # 调用数据库函数
        # 确保数据库返回的路径是SQL风格
        
        for file in files:
            if 'absolute_path' in file:
                file['absolute_path'] = file['absolute_path'].replace('\\', '/')
    except Exception as e:
        raise RuntimeError(f"数据库查询失败: {str(e)}")
        
    # 3. 调用AI分类器获取匹配文件
    try:
        """print("="*20)
        print(files)
        print("="*20)
        print("="*20)
        print(query)
        print("="*20)"""
        classifier = FileClassifier(API_KEY)  # 实例化
        match_files = classifier.get_match_files(query, files)
    except Exception as e:
        raise RuntimeError(f"AI匹配过程出错: {str(e)}")
    
    # 5. 获取目标文件详细信息
    try:
        """print("="*20)
        print(match_files)
        print("="*20)"""

        result_files = get_search_target_files(match_files)
        # 确保最终结果的路径是SQL风格
        for file in result_files:
            if 'file_path' in file:
                file['file_path'] = file['file_path'].replace('\\', '/')
    except Exception as e:
        raise RuntimeError(f"文件信息获取失败: {str(e)}")
    
    # 6. 返回最终结果（所有路径已标准化）
    return result_files