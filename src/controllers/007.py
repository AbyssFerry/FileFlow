import os
import shutil
import tempfile
from move_file import FileMover  # 假设上面的代码保存在file_mover.py中

def test_file_mover():
    """测试文件移动功能"""
    
    print("=== 开始文件移动测试 ===")
    input("按Enter键继续...")
    
    # 1. 创建临时测试目录
    print("\n步骤1: 创建测试目录")
    source_dir = tempfile.mkdtemp(prefix="source_")
    target_dir = tempfile.mkdtemp(prefix="target_")
    print(f"已创建源目录: {source_dir}")
    print(f"已创建目标目录: {target_dir}")
    input("按Enter键继续...")
    
    # 2. 在源目录中创建测试文件
    print("\n步骤2: 创建测试文件")
    test_file = os.path.join(source_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("这是一个测试文件")
    print(f"已创建测试文件: {test_file}")
    input("按Enter键继续...")
    
    # 3. 准备移动参数
    print("\n步骤3: 准备移动参数")
    file_info = {
        "文件旧路径": test_file,
        "文件新路径": os.path.join(target_dir, "moved_test.txt")
    }
    print(f"移动参数: {file_info}")
    input("按Enter键继续...")
    
    # 4. 执行移动操作
    print("\n步骤4: 执行移动操作")
    result = FileMover.move_file(file_info)
    print(f"移动结果: {'成功' if result else '失败'}")
    input("按Enter键继续...")
    
    # 5. 验证结果
    print("\n步骤5: 验证结果")
    print(f"源文件是否存在: {os.path.exists(file_info['文件旧路径'])}")
    print(f"目标文件是否存在: {os.path.exists(file_info['文件新路径'])}")
    input("按Enter键继续...")
    
    # 6. 清理测试环境
    print("\n步骤6: 清理测试环境")
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    print("已清理测试目录")
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_file_mover()