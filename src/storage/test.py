import os
from database_build import * 
from database import *


# 测试数据
test_directory_name = "test_directory"
test_directory_path = "/path/to/test/directory"
test_file_name = "test_file.txt"
test_file_path = "/path/to/test/file.txt"
test_extension = "txt"
test_size = 1024
test_content = "This is a test file content."
test_short_content = "Test file content."

# 测试文件操作
def test_file_operations():
    print("===== 测试文件操作 =====")
    # 插入文件
    print("插入文件测试：")
    success, message = insert_file(test_file_name, test_file_path, test_extension, test_size, test_content, test_short_content)
    print(message)

    print("插入文件测试：")
    success, message = insert_file("123123213", "/path/to/test/213123.txt", test_extension, test_size, test_content, test_short_content)
    print(message)

    # 查询文件
    print("查询文件测试：")
    files = query_files()
    for file in files:
        print(file)
    
    # 更新文件信息
    print("更新文件信息测试：")
    success, message = update_file_ai_description_by_path(test_file_path, "已分析")
    print(message)

    print("查询文件测试：")
    files = query_files()
    for file in files:
        print(file)   
 
    # 更新文件内容
    success, message = update_file_content_by_path(test_file_path, "Updated content")
    print(message)

    print("查询文件测试：")
    files = query_files()
    for file in files:
        print(file)

    # 删除文件
    print("删除文件测试：")
    delete_file(test_file_name)
    print(f"文件 '{test_file_name}' 删除成功")

    print("删除文件测试：")
    delete_file("123123213")
    print(f"文件 '123123213' 删除成功")

# 测试目录操作
def test_directory_operations():
    print("\n===== 测试目录操作 =====")
    
    # 插入目录
    print("插入目录测试：")
    success, message = insert_directory(test_directory_name, test_directory_path, test_size, "待分析")
    print(message)

    # 插入目录
    print("插入目录测试：")
    success, message = insert_directory("2123", "/path/to/test/123123", test_size, "待分析")
    print(message)
    
    # 查询目录
    print("查询目录测试：")
    directories = query_directories()
    for directory in directories:
        print(directory)
    
    # 更新目录信息
    print("更新目录信息测试：")
    success, message = update_directory_ai_description_by_path(test_directory_path, "已分析")
    print(message)

    # 查询目录
    print("查询目录测试：")
    directories = query_directories()
    for directory in directories:
        print(directory)

    # 更新目录大小
    success, message = update_directory_size_by_path(test_directory_path, 2048)
    print(message)

    # 查询目录
    print("查询目录测试：")
    directories = query_directories()
    for directory in directories:
        print(directory)

    # 删除目录
    print("删除目录测试：")
    delete_directory_by_path(test_directory_path)
    print(f"目录 '{test_directory_path}' 删除成功")

    # 删除目录
    print("删除目录测试：")
    delete_directory_by_path("/path/to/test/123123")
    print(f"目录 '/path/to/test/123123' 删除成功")

# 运行所有测试
def run_tests():
    test_file_operations()
    test_directory_operations()

if __name__ == "__main__":
    run_tests()
