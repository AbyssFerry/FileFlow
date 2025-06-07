import os
from parse_folder_path import parse_folder_path

# 输入文件夹路径
input_directory = r"D:\2023级计科2班(备份日期2025年5月1日)"
# 输出文件路径
output_file = r"D:\file-flow\src\controllers\text.txt"

def write_file_info_to_txt(file_info_list, output_path):
    """将文件信息列表写入文本文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for idx, file_info in enumerate(file_info_list, 1):
            f.write(f"文件 {idx}:\n")
            f.write(f"名称: {file_info['name']}\n")
            f.write(f"绝对路径: {file_info['absolute_path']}\n")
            f.write(f"扩展名: {file_info['extension']}\n")
            f.write(f"创建时间: {file_info['created_time']}\n")
            f.write(f"大小(字节): {file_info['size_bytes']}\n")
            f.write("内容:\n")
            f.write("-" * 50 + "\n")
            f.write(file_info['content'] + "\n")
            f.write("-" * 50 + "\n\n")

def main():
    # 检查输入目录是否存在
    if not os.path.exists(input_directory):
        print(f"错误: 目录 '{input_directory}' 不存在")
        return
    
    if not os.path.isdir(input_directory):
        print(f"错误: '{input_directory}' 不是目录")
        return
    
    # 解析文件夹
    print(f"正在解析目录: {input_directory}")
    file_info_list = parse_folder_path(input_directory)
    
    # 写入输出文件
    write_file_info_to_txt(file_info_list, output_file)
    print(f"解析完成，结果已写入: {output_file}")

if __name__ == "__main__":
    main()