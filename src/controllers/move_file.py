import os
import shutil

def move_file(fileNewPath):
    # 标准化输入路径为SQL风格
    absolute_path = fileNewPath["absolute_path"].replace('\\', '/')
    new_absolute_path = fileNewPath["new_absolute_path"].replace('\\', '/')
    reason_for_move = fileNewPath["reason_for_move"]
    name = fileNewPath["name"]
    
    # 创建目录结构（自动处理路径分隔符）
    new_dir = os.path.dirname(new_absolute_path)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir, exist_ok=True)
    
    try:
        # 移动文件（Python的shutil.move自动处理不同OS的路径分隔符）
        shutil.move(absolute_path, new_absolute_path)
        
        # 返回标准化后的路径
        newPath_and_reason = {
            "name": name,
            "new_absolute_path": new_absolute_path,  # 确保返回统一格式
            "reason_for_move": reason_for_move
        }
        return newPath_and_reason
    
    except Exception as e:
        # 错误处理（包含原始路径信息用于调试）
        raise RuntimeError(
            f"Failed to move file from {absolute_path} to {new_absolute_path}. Error: {str(e)}"
        )