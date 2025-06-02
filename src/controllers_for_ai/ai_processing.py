import os
from typing import List, Dict, Any
from api_keys import DEEPSEEK_API_KEY as deepseek_api_key
os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

class FileClassifier:
    def __init__(self):
        self.llm = ChatDeepSeek(model="deepseek-chat")

    def _invoke_chain(self, prompt: str) -> str:
        """统一的链式调用，便于异常处理和后续扩展"""
        chain = self.llm | parser
        try:
            return chain.invoke(prompt)
        except Exception as e:
            return f"LLM调用异常: {e}"

    def summary_file(self, name: str, path: str, content: str) -> Dict[str, str]:
        prompt = (
            f"请阅读以下文件内容：\n"
            f"文件名: {name}\n"
            f"文件路径: {path}\n"
            f"文件内容:\n{content}\n\n"
            f"请只输出详细总结和一句话描述，中间用换行分隔，不要输出其他内容（包括“详细总结”和“一句话描述”）。"
        )
        response = self._invoke_chain(prompt)
        try:
            summary, description = response.split('\n', 1)
        except Exception:
            summary, description = response, ""
        return {
            "summary": summary.strip(),
            "description": description.strip()
        }

    def classify_files(self, files: List[Dict[str, Any]]) -> str:
        prompt = (
            "你是一个文件分类助手。请根据每个文件的总结内容，将它们分为合适的类别（按照中图法）。"
            "对于每个类别，请给出：\n"
            "1. 类别名\n"
            "2. 该类别的简要描述\n"
            "3. 属于该类别的文件的绝对路径列表\n\n"
            "输出格式为JSON对象，每个键为类别名，值为包含'description'和'files'两个字段的对象，"
            "'description'为类别描述，'files'为该类别下所有文件的绝对路径列表。\n\n"
            "文件列表：\n"
        )
        prompt += "".join(
            f"{idx}. 文件名: {file['name']}\n路径: {file['path']}\n总结: {file['summary']}\n\n"
            for idx, file in enumerate(files, 1)
        )
        prompt += "请只输出JSON对象，不要输出其他内容。"
        return self._invoke_chain(prompt)

    def classify_file(
        self, name: str, path: str, summary: str, categories: List[Dict[str, Any]]
    ) -> str:
        prompt = (
            "你是一个文件归类助手。请根据文件的总结内容和已有目录的信息，判断该文件最适合归属哪个目录。\n"
            "如果没有合适的目录，请为该文件新建一个目录，并给出新目录的名称、描述和建议路径。\n"
            "请详细说明你的归类理由。\n"
            "输出格式为JSON对象，包含以下字段：\n"
            "category_name, category_description, category_path, reason, is_new。\n\n"
            "文件信息：\n"
            f"文件名: {name}\n"
            f"文件路径: {path}\n"
            f"文件总结: {summary}\n\n"
            "已有目录列表：\n"
        )
        prompt += "".join(
            f"{idx}. 目录名: {cat['name']}\n目录描述: {cat['description']}\n目录路径: {cat['path']}\n\n"
            for idx, cat in enumerate(categories, 1)
        )
        prompt += "请只输出JSON对象，不要输出其他内容。"
        return self._invoke_chain(prompt)

    def get_match_files(self, query: str, categories: List[Dict[str, Any]]) -> str:
        prompt = (
            "你是一个文件检索助手。请根据用户的查询，从所有目录及其文件中找出最符合查询的文件。\n"
            "每个目录包含目录名、描述、路径和文件列表。\n"
            "请返回所有匹配的文件的绝对路径列表，输出格式为JSON数组，只包含文件路径，不要输出其他内容。\n\n"
            f"用户查询: {query}\n\n"
            "目录及文件信息：\n"
        )
        prompt += "".join(
            f"{idx}. 目录名: {cat['name']}\n目录描述: {cat['description']}\n目录路径: {cat['path']}\n文件列表: {cat.get('files', [])}\n\n"
            for idx, cat in enumerate(categories, 1)
        )
        prompt += "请只输出JSON数组，不要输出其他内容。"
        return self._invoke_chain(prompt)

# ...existing code...

if __name__ == "__main__":
    # 示例文件
    files = [
        {
            "name": "GPA_Calculation.xlsx",
            "path": "d:/DataBaseWork/file-flow/GPA_Calculation.xlsx",
            "content": "",
            "summary": "这是一个用于计算大学生绩点的Excel表格。"
        },
        {
            "name": "Comprehensive_Quality_Report.docx",
            "path": "d:/DataBaseWork/file-flow/Comprehensive_Quality_Report.docx",
            "content": "",
            "summary": "这是一个大学生综合素质测评报告Word文档。"
        },
        {
            "name": "Physical_Test_Scores.xlsx",
            "path": "d:/DataBaseWork/file-flow/Physical_Test_Scores.xlsx",
            "content": "",
            "summary": "这是一个大学生体测成绩Excel表格。"
        },
        {
            "name": "Computer_Network_Exam_Results.xlsx",
            "path": "d:/DataBaseWork/file-flow/Computer_Network_Exam_Results.xlsx",
            "content": "",
            "summary": "这是一个计算机网络课程考试成绩Excel表格。"
        },
        {
            "name": "Internship_Report.docx",
            "path": "d:/DataBaseWork/file-flow/Internship_Report.docx",
            "content": "",
            "summary": "这是一个大学生实习报告Word文档。"
        },
        {
            "name": "Graduation_Thesis.docx",
            "path": "d:/DataBaseWork/file-flow/Graduation_Thesis.docx",
            "content": "",
            "summary": "这是一个大学生毕业论文Word文档。"
        },
        {
            "name": "English_Level_Test_Scores.xlsx",
            "path": "d:/DataBaseWork/file-flow/English_Level_Test_Scores.xlsx",
            "content": "",
            "summary": "这是一个大学英语等级考试成绩Excel表格。"
        },
        {
            "name": "Scholarship_Application_Form.docx",
            "path": "d:/DataBaseWork/file-flow/Scholarship_Application_Form.docx",
            "content": "",
            "summary": "这是一个奖学金申请表Word文档。"
        },
        {
            "name": "Class_Presentation.pptx",
            "path": "d:/DataBaseWork/file-flow/Class_Presentation.pptx",
            "content": "",
            "summary": "这是一个大学课堂演示PPT文件。"
        },
        {
            "name": "Lab_Report_Template.docx",
            "path": "d:/DataBaseWork/file-flow/Lab_Report_Template.docx",
            "content": "",
            "summary": "这是一个实验报告模板Word文档。"
        },
        {
            "name": "Student_Resume.docx",
            "path": "d:/DataBaseWork/file-flow/Student_Resume.docx",
            "content": "",
            "summary": "这是一个大学生简历Word文档。"
        },
        {
            "name": "Course_Schedule.xlsx",
            "path": "d:/DataBaseWork/file-flow/Course_Schedule.xlsx",
            "content": "",
            "summary": "这是一个大学生课程表Excel文件。"
        },
        {
            "name": "Academic_Transcript.pdf",
            "path": "d:/DataBaseWork/file-flow/Academic_Transcript.pdf",
            "content": "",
            "summary": "这是一个大学生成绩单PDF文件。"
        },
        {
            "name": "Project_Proposal.docx",
            "path": "d:/DataBaseWork/file-flow/Project_Proposal.docx",
            "content": "",
            "summary": "这是一个大学生项目立项书Word文档。"
        },
        {
            "name": "Volunteer_Hours_Record.xlsx",
            "path": "d:/DataBaseWork/file-flow/Volunteer_Hours_Record.xlsx",
            "content": "",
            "summary": "这是一个大学生志愿服务时长记录Excel表格。"
        },
        {
            "name": "Research_Paper.pdf",
            "path": "d:/DataBaseWork/file-flow/Research_Paper.pdf",
            "content": "",
            "summary": "这是一个大学生科研论文PDF文件。"
        },
        {
            "name": "Club_Activity_Summary.docx",
            "path": "d:/DataBaseWork/file-flow/Club_Activity_Summary.docx",
            "content": "",
            "summary": "这是一个大学生社团活动总结Word文档。"
        },
        {
            "name": "Competition_Award_Certificate.pdf",
            "path": "d:/DataBaseWork/file-flow/Competition_Award_Certificate.pdf",
            "content": "",
            "summary": "这是一个大学生竞赛获奖证书PDF文件。"
        },
        {
            "name": "Semester_Plan.docx",
            "path": "d:/DataBaseWork/file-flow/Semester_Plan.docx",
            "content": "",
            "summary": "这是一个大学生学期计划Word文档。"
        },
        {
            "name": "Graduation_Defense_Presentation.pptx",
            "path": "d:/DataBaseWork/file-flow/Graduation_Defense_Presentation.pptx",
            "content": "",
            "summary": "这是一个大学生毕业答辩PPT文件。"
        }
    ]

    categories = []

    classifier = FileClassifier()

    # 测试 summary_file
    print("测试 summary_file:")
    result = classifier.summary_file(files[0]["name"], files[0]["path"], files[0]["content"])
    print(result)

    # 测试 classify_files
    print("\n测试 classify_files:")
    result = classifier.classify_files(files)
    print(result)

    # 测试 classify_file
    print("\n测试 classify_file:")
    result = classifier.classify_file(files[0]["name"], files[0]["path"], files[0]["summary"], categories)
    print(result)

    # 测试 get_match_files
    print("\n测试 get_match_files:")
    result = classifier.get_match_files("Python", categories)
    print(result)