import unittest
from get_search_target_files import FileSearcher
class TestFileSearcher(unittest.TestCase):
    def test_find_matching_files(self):
        # 准备测试数据（根据图片中的JSON数据）
        small_list = [
            {
                "file_name": "2024年春季学期课程表.xlsx",
                "path": "/home/user/university_files/2024年春季学期课程表.xlsx"
            }
        ]
        
        large_list = [
            {
                "id": 1,
                "name": "2024年春季学期课程表",
                "absolute_path": "/home/user/university_files/2024年春季学期课程表.xlsx",
                "extension": "xlsx",
                "created_time": "2024-01-10 09:00:00",
                "modified_time": "2024-01-15 16:30:00",
                "size": 102400,
                "ai_description": "2024年春季学期的课程安排表，方便学生和教师查阅上课时间和地点。",
                "content": "包含2024年春季学期所有课程的时间安排、授课教师及教室信息。",
                "short_content": "2024春季课程表"
            },
            {
                "id": 2,
                "name": "学生手册（2024版）",
                "absolute_path": "/home/user/university_files/学生手册（2024版）.pdf",
                "extension": "pdf",
                "created_time": "2024-01-05 14:20:00",
                "modified_time": "2024-01-07 11:10:00",
                "size": 256000,
                "ai_description": "2024年更新版学生手册，涵盖校规校纪及学生生活指导内容。",
                "content": "包含学校规章制度、学生行为规范及校园生活相关指导内容。",
                "short_content": "2024学生手册"
            }
        ]
        
        # 调用被测试方法
        result = FileSearcher.find_matching_files(large_list, small_list)
        
        print(result)
        # 验证结果
        self.assertEqual(len(result), 1)  # 应该只匹配到一个文件
        matched_file = result[0]
        
        # 验证五个关键字段
        self.assertEqual(matched_file["name"], "2024年春季学期课程表")
        self.assertEqual(matched_file["absolute_path"], "/home/user/university_files/2024年春季学期课程表.xlsx")
        self.assertEqual(matched_file["extension"], "xlsx")
        self.assertEqual(matched_file["size"], "102400")
        self.assertEqual(matched_file["ai_description"], "2024年春季学期的课程安排表，方便学生和教师查阅上课时间和地点。")

if __name__ == "__main__":
    unittest.main()