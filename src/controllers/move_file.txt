import os
import shutil
from typing import Dict

class FileMover:
    """文件移动模块"""
    
    @staticmethod
    def move_file(file_info: Dict[str, str]) -> bool:
        """
        核心移动功能
        
        参数:
            file_info: 必须包含路径字段:
                {
                    "文件新路径": "/target/path/file.txt",  # 必须
                    "文件旧路径": "/source/path/file.txt"   # 必须
                }
        
        返回:
            bool: 移动是否成功
        """
        try:
            # 验证必要字段
            if not all(key in file_info for key in ["文件新路径", "文件旧路径"]):
                raise ValueError("缺少必要路径参数")
            
            src = file_info["文件旧路径"]
            dst = file_info["文件新路径"]
            
            # 检查源文件存在性
            if not os.path.exists(src):
                raise FileNotFoundError(f"源文件不存在: {src}")
            
            # 创建目标目录
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            # 执行移动
            shutil.move(src, dst)
            return True
            
        except Exception as e:
            print(f"[文件移动失败] 错误: {type(e).__name__} - {str(e)}")
            return False