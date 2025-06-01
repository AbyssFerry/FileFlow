import os
import shutil
from typing import Dict, Optional

class FileOrganizer:
    """专门处理文件移动和目录创建"""
    @staticmethod
    def organize_files(file_info: Dict[str, str]) -> bool:
        """
        核心文件整理功能
        参数:
            file_info: 包含以下键的字典:
                - 'old_path': 文件原始绝对路径
                - 'new_path': 文件目标绝对路径
        
        返回:
            bool: 操作是否成功
        """
        try:
            # 验证必要参数存在
            if not all(key in file_info for key in ['old_path', 'new_path']):
                raise ValueError("缺少必要路径参数")
            
            old_path = file_info['old_path']
            new_path = file_info['new_path']
            
            # 检查源文件是否存在
            if not os.path.exists(old_path):
                raise FileNotFoundError(f"源文件不存在: {old_path}")
            
            # 创建目标目录（包括所有不存在的父目录）
            target_dir = os.path.dirname(new_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # 执行文件移动（可自动覆盖同名文件）
            shutil.move(old_path, new_path)
            return True
            
        except Exception as e:
            print(f"[文件整理失败] 错误类型: {type(e).__name__}, 详情: {str(e)}")
            return False