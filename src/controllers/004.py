import os
import shutil
import unittest
from organize_files import FileOrganizer

class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        """在指定目录创建测试文件夹和文件"""
        # 基础路径
        self.base_dir = r"D:\file-flow\src\controllers\beta"
        
        # 测试文件夹路径
        self.source_dir = os.path.join(self.base_dir, "test_source")
        self.target_dir = os.path.join(self.base_dir, "test_target")
        
        # 确保基础目录存在
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        
        # 创建测试文件夹
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.target_dir, exist_ok=True)
        
        # 创建测试文件
        self.test_file = os.path.join(self.source_dir, "test_file.txt")
        with open(self.test_file, 'w') as f:
            f.write("This is a test file.")
            
        print(f"\n测试环境已创建:")
        print(f"源文件夹: {self.source_dir}")
        print(f"目标文件夹: {self.target_dir}")
        print(f"测试文件: {self.test_file}")
        input("\n按回车键继续测试...")

    def tearDown(self):
        """清理测试文件夹"""
        try:
            if os.path.exists(self.source_dir):
                shutil.rmtree(self.source_dir)
            if os.path.exists(self.target_dir):
                shutil.rmtree(self.target_dir)
        except Exception as e:
            print(f"清理失败: {e}")
        
        print("\n测试环境已清理")

    def test_file_movement(self):
        """测试文件移动功能"""
        new_path = os.path.join(self.target_dir, "test_file.txt")
        file_info = {
            'old_path': self.test_file,
            'new_path': new_path
        }
        
        result = FileOrganizer.organize_files(file_info)
        
        self.assertTrue(result, "文件移动操作应返回True")
        self.assertTrue(os.path.exists(new_path), "文件应存在于目标路径")
        self.assertFalse(os.path.exists(self.test_file), "文件不应再存在于源路径")
        
        print("\n测试结果:")
        print(f"文件已成功从 {self.test_file} 移动到 {new_path}")

    def test_missing_parameters(self):
        """测试缺少必要参数的情况"""
        with self.assertRaises(ValueError):
            FileOrganizer.organize_files({'new_path': 'dummy_path'})
        
        with self.assertRaises(ValueError):
            FileOrganizer.organize_files({'old_path': 'dummy_path'})
            
        print("\n参数验证测试通过")

    def test_nonexistent_source(self):
        """测试源文件不存在的情况"""
        file_info = {
            'old_path': os.path.join(self.source_dir, "nonexistent.txt"),
            'new_path': os.path.join(self.target_dir, "dummy.txt")
        }
        
        result = FileOrganizer.organize_files(file_info)
        self.assertFalse(result, "对不存在的文件操作应返回False")
        print("\n不存在的源文件测试通过")

if __name__ == '__main__':
    unittest.main(verbosity=2)