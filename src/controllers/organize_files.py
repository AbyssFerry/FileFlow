import os
import shutil
from src.ui.uiprint import print

def organize_files(files):
    """
    将文件从原路径移动到新路径，使用SQL风格路径格式(正斜杠/)
    如果新路径不存在则创建目录
    
    Args:
        files (list): 文件信息列表，每个元素是包含文件信息的字典
            [
                {
                    "name": "",
                    "absolute_path": "",       # 自动转为正斜杠格式
                    "new_absolute_path": "",   # 自动转为正斜杠格式
                    ...
                }
            ]
    
    Returns:
        tuple: (bool, str) 
            - 第一个元素表示整体是否成功 (True/False)
            - 第二个元素是详细的执行结果描述
    """
    print("开始组织文件...")
    print(f"需要处理的文件数量: {len(files)}")
    success_count = 0
    failure_count = 0
    details = []
    
    for index, file_info in enumerate(files, 1):
        print(f"处理文件 {index}/{len(files)}: {file_info['name']}")
        # 标准化路径为SQL风格(正斜杠)
        source_path = file_info["absolute_path"].replace('\\', '/')
        dest_path = file_info["new_absolute_path"].replace('\\', '/')
        
        # 确保源文件存在
        if not os.path.exists(source_path):
            msg = f"警告: 源文件不存在，跳过: {source_path}"
            print(msg)
            details.append(msg)
            failure_count += 1
            continue
        
        # 创建目标目录（如果不存在）
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            print(f"目录不存在，正在创建: {dest_dir}")
            try:
                os.makedirs(dest_dir, exist_ok=True)
                msg = f"已创建目录: {dest_dir}"
                print(msg)
                details.append(msg)
            except OSError as e:
                msg = f"错误: 无法创建目录 {dest_dir}: {str(e)}"
                print(msg)
                details.append(msg)
                failure_count += 1
                continue
        
        # 移动文件
        print(f"正在移动文件: {source_path} -> {dest_path}")
        try:
            shutil.move(source_path, dest_path)
            msg = f"成功移动: {source_path} -> {dest_path}"
            print(msg)
            details.append(msg)
            success_count += 1
        except Exception as e:
            msg = f"错误: 无法移动文件 {source_path} 到 {dest_path}: {str(e)}"
            print(msg)
            details.append(msg)
            failure_count += 1
    
    # 生成结果报告
    print("\n正在生成结果报告...")
    result_msg = "\n".join([
        "="*40,
        f"操作完成 (成功: {success_count}, 失败: {failure_count})",
        "="*40,
        *details,
        "="*40
    ])
    
    print(f"文件组织结束 - 成功: {success_count}, 失败: {failure_count}")
    # 返回处理结果
    if failure_count == 0:
        return (True, result_msg)
    elif success_count > 0:
        return (False, result_msg)
    else:
        return (False, result_msg)