import unittest
import os
import shutil
from datetime import datetime
from parser_file import parse_file, parse_folder, save_to_db, get_directories

class TestFileParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 用户指定的输入目录
        cls.input_dir = r"D:\2023级计科2班(备份日期2025年5月1日)"
        
        # 用户指定的输出文件
        cls.output_file = r"D:\file-flow\src\controllers\text.txt"
        os.makedirs(os.path.dirname(cls.output_file), exist_ok=True)
        
        # 图片中提供的测试数据
        cls.test_data = [
            {
                "name": "WorkAndStudy",
                "absolute_path": "/home/user/WorkAndStudy",
                "created_time": "2025-06-02 12:30:45",
                "size": "1048576",
                "ai_description": "用于存放学习资料、工作文件和个人项目相关文档。"
            },
            {
                "name": "LifePhotos",
                "absolute_path": "/home/user/LifePhotos",
                "created_time": "2025-06-01 08:45:30",
                "size": "2097152",
                "ai_description": "保存生活照片、旅行记录和各类视频创作素材。"
            },
            {
                "name": "WebDownloads",
                "absolute_path": "/home/user/WebDownloads",
                "created_time": "2025-05-30 16:20:15",
                "size": "5242880",
                "ai_description": "集中保存从浏览器、邮件或平台获取的临时文件和资料。"
            },
            {
                "name": "学生手册.pdf",
                "absolute_path": "/home/user/学生手册.pdf",
                "created_time": "2025-06-02 12:30:45",
                "size": "1048576",
                "content": "根据《德意慈教教育基金评选办法》，经学生申请、学院评审，拟推荐以下2名学生:\n1. 张三(学号:20231001)\n2. 李四(学号:20231002)\n公示时间:2024年3月15日-3月17日\n如有异议，请联系学院办公室王老师，电话:12345678\n计算机与网络空间安全学院\n2024年3月15日"
            }
        ]

    def test_parse_real_directory(self):
        """测试真实目录解析功能"""
        # 确保输入目录存在
        self.assertTrue(os.path.exists(self.input_dir), f"输入目录不存在: {self.input_dir}")
        
        # 解析目录中的所有文件
        results = parse_folder(self.input_dir)
        
        # 将结果写入输出文件
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # 写入测试头部信息
            f.write("="*50 + "\n")
            f.write("文件解析测试报告\n")
            f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"输入目录: {self.input_dir}\n")
            f.write("="*50 + "\n\n")
            
            # 写入左下角参数列表
            param_list = ["name", "absolute_path", "extension", "created_time", "size_bytes", "content"]
            f.write("左下角参数列表:\n")
            f.write(str(param_list) + "\n\n")
            
            # 写入每个文件的信息
            f.write("文件详细信息:\n")
            for result in results:
                f.write(f"文件名: {result['name']}\n")
                f.write(f"绝对路径: {result['absolute_path']}\n")
                f.write(f"扩展名: {result['extension']}\n")
                f.write(f"创建时间: {result['created_time']}\n")
                f.write(f"大小(字节): {result['size_bytes']}\n")
                f.write(f"内容预览: {result['content'][:200]}...\n")
                f.write("-"*50 + "\n")
            
            # 写入图片中的公示信息
            f.write("\n公示文件验证:\n")
            for data in self.test_data:
                if "学生手册" in data["name"]:
                    f.write(f"文件名称: {data['name']}\n")
                    f.write(f"文件内容: \n{data['content']}\n")
                    f.write("-"*50 + "\n")
            
            # 写入数据库测试结果
            f.write("\n数据库功能测试:\n")
            test_db = "test_file_database.db"
            save_to_db(results, test_db)
            directories = get_directories(test_db)
            f.write("数据库目录信息:\n")
            for dir_info in directories:
                f.write(f"目录路径: {dir_info['path']}\n")
                f.write(f"目录描述: {dir_info['description']}\n")
            
            # 清理测试数据库
            if os.path.exists(test_db):
                os.remove(test_db)

        print(f"测试完成，结果已保存到: {self.output_file}")

    def test_parse_file_parameters(self):
        """验证parse_file返回的参数完整性"""
        # 在输入目录中找一个测试文件
        test_files = [f for f in os.listdir(self.input_dir) if os.path.isfile(os.path.join(self.input_dir, f))]
        if test_files:
            test_file = os.path.join(self.input_dir, test_files[0])
            result = parse_file(test_file)
            
            # 验证返回的字典包含所有必需的键
            required_params = ["name", "absolute_path", "extension", "created_time", "size_bytes", "content"]
            for param in required_params:
                self.assertIn(param, result)
            
            # 验证特定值
            self.assertEqual(result["name"], os.path.basename(test_file))
            self.assertEqual(result["absolute_path"], os.path.abspath(test_file))
            self.assertTrue(result["extension"].startswith('.'))
            self.assertIsInstance(result["created_time"], str)
            self.assertIsInstance(result["size_bytes"], int)
            self.assertIsInstance(result["content"], str)

if __name__ == '__main__':
    unittest.main(verbosity=2)