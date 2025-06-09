import os
import shutil

def organize_files(files):
    """
    将文件从原路径移动到新路径，如果新路径不存在则创建目录
    
    Args:
        files (list): 文件信息列表，每个元素是一个包含文件信息的字典
            [
                {
                    "name": "",
                    "absolute_path": "",
                    "new_absolute_path": "",
                    ...
                }
            ]
    
    Returns:
        tuple: (bool, str) 
            - 第一个元素表示整体是否成功 (True/False)
            - 第二个元素是详细的执行结果描述
    """
    success_count = 0
    failure_count = 0
    
    for file_info in files:
        source_path = file_info["absolute_path"]
        dest_path = file_info["new_absolute_path"]
        
        # 确保源文件存在
        if not os.path.exists(source_path):
            print(f"警告: 源文件不存在，跳过: {source_path}")
            failure_count += 1
            continue
        
        # 创建目标目录（如果不存在）
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
                print(f"已创建目录: {dest_dir}")
            except OSError as e:
                print(f"错误: 无法创建目录 {dest_dir}: {e}")
                failure_count += 1
                continue
        
        # 移动文件
        try:
            shutil.move(source_path, dest_path)
            print(f"已移动文件: {source_path} -> {dest_path}")
            success_count += 1
        except Exception as e:
            print(f"错误: 无法移动文件 {source_path} 到 {dest_path}: {e}")
            failure_count += 1
    
    # 返回处理结果
    if failure_count == 0:
        return (True, "所有文件处理成功")
    elif success_count > 0:
        return (False, f"部分文件处理成功（成功：{success_count}，失败：{failure_count}）")
    else:
        return (False, "所有文件处理失败")