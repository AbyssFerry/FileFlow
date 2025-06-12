import sys
import os
from typing import List, Dict, Any
from src.controllers.get_search_target_files import get_search_target_files
from src.ui.uiprint import print
# 标准化项目根路径为SQL风格
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')
sys.path.append(project_root)

from src.controllers_for_ai.ai_processing import FileClassifier
from src.storage.database import fileShow, fileDeleteByPath
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
    print(f"\n===== 开始搜索: '{query}' =====")
    
    # 1. 接收查询参数（通过函数形参query已接收）
    print(f"步骤1: 已接收搜索查询: '{query}'")
    
    # 2. 调用数据库获取所有文件
    print("步骤2: 正在从数据库获取文件列表...")
    try:
        files = fileShow()  # 调用数据库函数
        # 确保数据库返回的路径是SQL风格
        
        for file in files:
            if 'absolute_path' in file:
                file['absolute_path'] = file['absolute_path'].replace('\\', '/')
        print(f"成功获取 {len(files)} 个文件记录")
        
        # 检查文件是否存在于文件系统
        print("正在检查文件是否存在...")
        missing_files = []
        for file in files[:]:  # 使用切片创建副本，因为我们会在循环中修改 files
            path = file.get('absolute_path')
            if path and not os.path.exists(path):
                print(f"文件不存在，从数据库中删除: {path}")
                try:
                    fileDeleteByPath(path)
                    missing_files.append(path)
                    files.remove(file)  # 从列表中移除不存在的文件
                except Exception as e:
                    print(f"删除文件记录失败: {path}, 错误: {str(e)}")
        if missing_files:
            print(f"已从数据库中删除 {len(missing_files)} 个不存在的文件记录")
        print(f"剩余有效文件记录: {len(files)}")
    except Exception as e:
        print(f"错误: 数据库查询失败: {str(e)}")
        raise RuntimeError(f"数据库查询失败: {str(e)}")



    # 3. 调用AI分类器获取匹配文件
    print("\n步骤3: 正在使用AI匹配相关文件...")
    print("初始化AI模型...")
    try:
        classifier = FileClassifier(API_KEY)  # 实例化
        print("AI模型已初始化，开始搜索匹配文件...")
        match_files = classifier.get_match_files(query, files)
        print(f"AI匹配完成，找到 {len(match_files)} 个相关文件")
    except Exception as e:
        print(f"错误: AI匹配过程出错: {str(e)}")
        raise RuntimeError(f"AI匹配过程出错: {str(e)}")
    
    # 5. 获取目标文件详细信息
    print("\n步骤4: 获取匹配文件的详细信息...")
    try:
        result_files = get_search_target_files(match_files)

        # 去除 file_path 重复的文件
        seen_paths = set()
        unique_files = []
        for file in result_files:
            path = file.get('file_path')
            if path and path not in seen_paths:
                unique_files.append(file)
                seen_paths.add(path)
        result_files = unique_files

        # 确保最终结果的路径是SQL风格
        for file in result_files:
            if 'file_path' in file:
                file['file_path'] = file['file_path'].replace('\\', '/')
        print(f"成功获取 {len(result_files)} 个文件的详细信息")
    except Exception as e:
        print(f"错误: 文件信息获取失败: {str(e)}")
        raise RuntimeError(f"文件信息获取失败: {str(e)}")
    
    # 6. 返回最终结果（所有路径已标准化）
    print("\n===== 搜索完成，返回结果 =====")
    return result_files