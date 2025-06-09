import os
import shutil

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
    success_count = 0
    failure_count = 0
    details = []
    
    for file_info in files:
        # 标准化路径为SQL风格(正斜杠)
        source_path = file_info["absolute_path"].replace('\\', '/')
        dest_path = file_info["new_absolute_path"].replace('\\', '/')
        
        # 确保源文件存在
        if not os.path.exists(source_path):
            msg = f"警告: 源文件不存在，跳过: {source_path}"
            details.append(msg)
            failure_count += 1
            continue
        
        # 创建目标目录（如果不存在）
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
                msg = f"已创建目录: {dest_dir}"
                details.append(msg)
            except OSError as e:
                msg = f"错误: 无法创建目录 {dest_dir}: {str(e)}"
                details.append(msg)
                failure_count += 1
                continue
        
        # 移动文件
        try:
            shutil.move(source_path, dest_path)
            msg = f"成功移动: {source_path} -> {dest_path}"
            details.append(msg)
            success_count += 1
        except Exception as e:
            msg = f"错误: 无法移动文件 {source_path} 到 {dest_path}: {str(e)}"
            details.append(msg)
            failure_count += 1
    
    # 生成结果报告
    result_msg = "\n".join([
        "="*40,
        f"操作完成 (成功: {success_count}, 失败: {failure_count})",
        "="*40,
        *details,
        "="*40
    ])
    
    # 返回处理结果
    if failure_count == 0:
        return (True, result_msg)
    elif success_count > 0:
        return (False, result_msg)
    else:
        return (False, result_msg)