import os
import shutil
from src.ui.uiprint import print
def move_file(fileNewPath):
    # 标准化输入路径为SQL风格
    absolute_path = fileNewPath["absolute_path"].replace('\\', '/')
    new_absolute_path = fileNewPath["new_absolute_path"].replace('\\', '/')
    reason_for_move = fileNewPath["reason_for_move"]
    name = fileNewPath["name"]
    
    # 创建目录结构（自动处理路径分隔符）
    new_dir = os.path.dirname(new_absolute_path)
    if not os.path.exists(new_dir):
        print(f"创建目标目录: {new_dir}")
        os.makedirs(new_dir, exist_ok=True)
    
    # 检查目标文件是否已存在
    if os.path.exists(new_absolute_path):
        print(f"\n=== 移动文件 ===")
        print(f"文件名称: {name}")
        print(f"源路径: {absolute_path}")
        print(f"目标路径: {new_absolute_path}")
        print(f"⚠️ 目标位置已存在同名文件，跳过移动操作")
        
        # 即使不移动，也返回相同的结果结构
        newPath_and_reason = {
            "name": name,
            "new_absolute_path": '原本路径:' + new_absolute_path,
            "reason_for_move": '本文件已存在,未执行操作,上面的新路径为原本路径。'
        }
        return newPath_and_reason
    
    print(f"\n=== 移动文件 ===")
    print(f"文件名称: {name}")
    print(f"源路径: {absolute_path}")
    print(f"目标路径: {new_absolute_path}")
    print(f"移动原因: {reason_for_move}")
    print(f"开始移动...")
    
    try:
        # 移动文件（Python的shutil.move自动处理不同OS的路径分隔符）
        shutil.move(absolute_path, new_absolute_path)
        print(f"✅ 文件 '{name}' 移动成功!")
        
        # 返回标准化后的路径
        newPath_and_reason = {
            "name": name,
            "new_absolute_path": new_absolute_path,  # 确保返回统一格式
            "reason_for_move": reason_for_move
        }
        return newPath_and_reason
    
    except Exception as e:
        print(f"❌ 移动失败: 无法将文件从 {absolute_path} 移动到 {new_absolute_path}")
        print(f"错误信息: {str(e)}")
        # 错误处理（包含原始路径信息用于调试）
        raise RuntimeError(
            f"Failed to move file from {absolute_path} to {new_absolute_path}. Error: {str(e)}"
        )