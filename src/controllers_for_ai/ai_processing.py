import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Tuple
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = "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"
os.environ["LANGSMITH_PROJECT"] = "test_fileflow"

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
parser = StrOutputParser()

class FileClassifier:
    """智能文件归类与检索助手"""

    def __init__(self):
        # 修改初始化，将最大输出令牌数设置为8k
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            max_tokens=8192  # 将输出限制设为8k而不是默认的4k
        )

    def _invoke_chain(self, prompt: str) -> str:
        """调用大模型链，返回字符串结果"""
        chain = self.llm | parser
        try:
            return chain.invoke(prompt)
        except Exception as e:
            return f"LLM调用异常: {e}"

    def summary_file(self, file: Dict[str, Any]) -> Dict[str, Any]:
        """对单个文件生成详细总结和一句话描述"""
        prompt = (
            f"请阅读以下文件内容：\n"
            f"文件名: {file['name']}\n"
            f"文件内容:\n{file['content']}\n\n"
            f"请只输出详细总结和一句话描述，中间用换行分隔，不要输出其他内容（包括“详细总结”和“一句话描述”）。"
        )
        response = self._invoke_chain(prompt)
        try:
            ai_description, short_content = response.split('\n', 1)
        except Exception:
            ai_description, short_content = "", ""
        return {
            "name": file.get("name", ""),
            "absolute_path": file.get("absolute_path", ""),
            "new_absolute_path": file.get("new_absolute_path", ""),
            "extension": file.get("extension", ""),
            "created_time": file.get("created_time", ""),
            "size": file.get("size", 0),
            "content": file.get("content", ""),
            "ai_description": ai_description.strip(),
            "short_content": short_content.strip(),
            "reason_for_move": file.get("reason_for_move", "")
        }

    def classify_files(self, files: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """批量归类文件，返回归类后的文件和目录列表"""
        prompt = (
            "你是一个智能文件归类助手。请根据每个文件的内容和AI描述，将它们合理归入二到三级目录，并输出文件列表和目录列表：\n"
            "1. 文件列表，每个文件包含：name|@|@|absolute_path|@|@|new_absolute_path。\n"
            "2. 目录列表，每个目录包含：name|@|@|absolute_path|@|@|ai_description。\n"
            "注意：new_absolute_path为文件归类后的新路径，且必须以/开头，目录需体现二到三级结构。\n"
            "目录名只取最后一级目录名。\n"
            "文件数据如下：\n"
        )
        for idx, file in enumerate(files, 1):
            prompt += (
                f"{idx}. 文件名: {file['name']}\n"
                f"原路径: {file['absolute_path']}\n"
                f"AI描述: {file.get('ai_description', '')}\n\n"
            )
        prompt += (
            "请严格按照如下格式输出：\n"
            "不要输出“文件列表”和“目录列表”这八个字符\n"
            "文件列表的每个文件都用换行符分隔\n"
            "每个文件的每个属性都用|@|@|分隔\n"
            "文件列表和目录列表之间用==@==分隔。\n"
            "目录列表的每个目录都用换行符分隔\n"
            "每个目录的每个属性都用|@|@|分隔\n"
            "所有new_absolute_path必须以/开头。\n"
        )

        # 将prompt写入文件以便调试 @@@@
        # with open(r"D:\vs code\python\FileFlow\testdoc", "w", encoding="utf-8") as f:
        #     f.write(prompt)


        response = self._invoke_chain(prompt)
        try:
            files_str, categories_str = response.strip().split('==@==', 1)
            files_list_raw = [file.split('|@|@|') for file in files_str.strip().split('\n') if file.strip()]
            categories_list_raw = [cat.split('|@|@|') for cat in categories_str.strip().split('\n') if cat.strip()]
            files_list = []
            for file_item in files_list_raw:
                name, absolute_path, new_absolute_path = file_item
                origin = next((f for f in files if f['name'] == name and f['absolute_path'] == absolute_path), {})
                files_list.append({
                    "name": name,
                    "absolute_path": absolute_path,
                    "new_absolute_path": new_absolute_path,
                    "extension": origin.get("extension", ""),
                    "created_time": origin.get("created_time", ""),
                    "size": origin.get("size", 0),
                    "content": origin.get("content", ""),
                    "ai_description": origin.get("ai_description", ""),
                    "short_content": origin.get("short_content", ""),
                    "reason_for_move": origin.get("reason_for_move", "")
                })
            categories_list = []
            for cat_item in categories_list_raw:             
                name, absolute_path, ai_description = cat_item
                categories_list.append({
                    "name": name,
                    "absolute_path": absolute_path,
                    "created_time": "",
                    "register_time": "",
                    "size": 0,
                    "ai_description": ai_description,
                })
            return {"files": files_list, "categories": categories_list}
        except Exception as e:
            print(f"分类文件时发生异常: {e}")
            return {"files": [], "categories": []}

    def classify_file(
        self, file: Dict[str, Any], categories: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """将单个文件归入最合适的目录"""
        prompt = (
            "你是一个文件归类助手。请根据文件的内容、AI描述和所有目录的信息，判断该文件最适合归属哪个目录\n"
            "请输出文件的新绝对路径和归类原因。\n"
            "请严格按照如下格式输出：name|@|@|new_absolute_path|@|@|reason_for_move\n"
            "文件信息如下：\n"
            f"文件名: {file['name']}\n"
            f"AI描述: {file['ai_description']}\n"
            "所有目录信息如下：\n"
        )
        for cat in categories:
            prompt += (
                f"目录名: {cat['name']}\n"
                f"绝对路径: {cat['absolute_path']}\n"
                f"AI描述: {cat['ai_description']}\n\n"
            )
        response = self._invoke_chain(prompt)
        try:
            name, new_absolute_path, reason_for_move = [x.strip() for x in response.strip().split('|@|@|')]
            return {
                "name": name,
                "absolute_path": file.get("absolute_path", ""),
                "new_absolute_path": new_absolute_path,
                "extension": file.get("extension", ""),
                "created_time": file.get("created_time", ""),
                "size": file.get("size", 0),
                "content": file.get("content", ""),
                "ai_description": file.get("ai_description", ""),
                "short_content": file.get("short_content", ""),
                "reason_for_move": reason_for_move
            }
        except Exception as e:
            print(f"分类文件时发生异常: {e}")
            return file

    def get_match_files(self, query: str, files: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """根据查询检索最匹配的文件"""
        prompt = (
            "你是一个文件检索助手。请根据用户的查询，从所有文件中找出最符合查询的文件。\n"
            "请严格按照如下格式输出所有匹配的文件，每个文件一行：name|@|@|absolute_path\n"
            "不要输出其他内容。\n\n"
            f"用户查询: {query}\n\n"
            "文件信息如下：\n"
        )
        for file in files:
            prompt += (
                f"文件名: {file['name']}\n"
                f"绝对路径: {file['absolute_path']}\n"
                f"AI描述: {file.get('ai_description', '')}\n"
            )
        response = self._invoke_chain(prompt)
        result = []
        try:
            for line in response.strip().split('\n'):
                if not line.strip():
                    continue
                parts = line.strip().split('|@|@|')
                if len(parts) == 2:
                    name, absolute_path = parts
                    result.append({
                        "name": name.strip(),
                        "absolute_path": absolute_path.strip()
                    })
        except Exception as e:
            print(f"检索文件时发生异常: {e}")
        return result

def main():
    """主流程测试函数"""
    files = [
        {
            "name": "计算机与网络空间安全学院2023-2024学年德盛慈善教育基金拟推荐名单公示",
            "absolute_path": "/documents/计算机与网络空间安全学院2023-2024学年德盛慈善教育基金拟推荐名单公示.txt",
            "content": "计算机与网络空间安全学院\n2023-2024学年德盛慈善教育基金拟推荐名单公示\n\n根据《德盛慈善教育基金评选办法》，经学生申请、学院评审，拟推荐以下2名学生：\n\n1. 张三（学号：20231001），专业：网络空间安全，成绩优异，积极参与社会实践与志愿服务。\n2. 李四（学号：20231002），专业：计算机科学与技术，学习刻苦，担任班级学习委员。\n\n公示时间：2024年3月15日-3月17日\n如有异议，请联系学院办公室王老师，电话：12345678\n\n计算机与网络空间安全学院\n2024年3月15日"
        },
        {
            "name": "2024年上半年学术论文发表统计表",
            "absolute_path": "/documents/2024年上半年学术论文发表统计表.xlsx",
            "content": "论文题目,作者,期刊,发表时间,摘要\n深度学习在图像识别中的应用,王五,计算机学报,2024-03-10,本文探讨了深度学习在图像识别领域的最新进展与应用。\n区块链技术在金融安全中的应用,赵六,网络安全,2024-04-15,分析区块链技术在金融行业中的安全优势与挑战。\n人工智能驱动的智能医疗系统,孙七,人工智能,2024-05-20,介绍AI在医疗诊断和健康管理中的创新应用。"
        },
        {
            "name": "2023年度财务决算报告",
            "absolute_path": "/documents/2023年度财务决算报告.pdf",
            "content": "2023年度财务决算报告\n本年度收入总计1000万元，支出950万元，结余50万元。\n主要收入来源包括学费、科研经费及社会捐赠。支出主要用于教学、科研、基础设施建设及奖助学金发放。报告详细列举了各项收支明细，并对未来财务规划提出建议。"
        },
        {
            "name": "Python编程基础课程大纲",
            "absolute_path": "/documents/计算机学院/Python编程基础课程大纲.docx",
            "content": "课程目标：掌握Python基础语法、数据结构、文件操作与常用库。\n课程内容包括：变量与数据类型、流程控制、函数与模块、文件读写、异常处理、常用标准库（如os、sys、re）、简单项目实践。课程安排共16周，每周2学时，含实验与作业。"
        },
        {
            "name": "2024年春季学期课程表",
            "absolute_path": "/documents/2024年春季学期课程表.xlsx",
            "content": "周一：高等数学（8:00-9:40），教室A101；大学物理（10:00-11:40），教室A102。\n周二：大学英语（8:00-9:40），教室B201；Python编程基础（10:00-11:40），机房C301。\n周三：数据结构（8:00-9:40），教室A103；体育（14:00-15:40），操场。\n周四：离散数学（8:00-9:40），教室A104。\n周五：创新创业（10:00-11:40），教室B202。"
        },
        {
            "name": "学生会2024年工作计划",
            "absolute_path": "/documents/学生会2024年工作计划.docx",
            "content": "2024年学生会将重点开展学术交流、文体活动和志愿服务等工作。\n具体计划包括：举办学术讲座与竞赛、组织篮球赛和歌唱比赛、开展社区志愿服务、加强与兄弟院校学生会的交流合作、完善学生权益维护机制。"
        },
        {
            "name": "2024年校园招聘企业名单",
            "absolute_path": "/documents/2024年校园招聘企业名单.xlsx",
            "content": "企业名称,招聘岗位,联系方式,宣讲时间,备注\n华为,软件开发,123456789,2024-04-10 14:00,需本科及以上学历\n阿里巴巴,数据分析,987654321,2024-04-12 10:00,欢迎应届毕业生\n腾讯,产品经理,135792468,2024-04-15 09:00,有实习经验优先"
        },
        {
            "name": "2024年毕业生就业质量报告",
            "absolute_path": "/documents/2024年毕业生就业质量报告.pdf",
            "content": "2024年毕业生就业率达95%，主要就业方向为IT、金融、教育等行业。\n报告详细分析了毕业生就业单位类型、薪资水平、就业地区分布，并对未就业学生的原因进行了调研。"
        },
        {
            "name": "2024年实验室安全检查记录",
            "absolute_path": "/documents/2024年实验室安全检查记录.docx",
            "content": "2024年3月实验室安全检查，未发现重大安全隐患。\n检查内容包括：消防设施、用电安全、化学品存储、实验室卫生等。对存在的小问题已现场整改，并对相关责任人进行了安全培训。"
        },
        {
            "name": "2024年研究生招生简章",
            "absolute_path": "/documents/2024年研究生招生简章.pdf",
            "content": "2024年研究生招生简章\n招生专业：计算机科学与技术、网络空间安全、人工智能等。\n招生计划：全日制硕士100人，非全日制硕士30人。\n报考条件：本科及以上学历，具备相关专业背景。\n报名时间、考试安排及奖学金政策详见学院官网。"
        }
    ]

    classifier = FileClassifier()

    print("测试 summary_file:")
    files[0] = classifier.summary_file(files[0])
    print(files[0])

    print("测试 summary_file 对多个文件:")
    for idx, file in enumerate(files):
        files[idx] = classifier.summary_file(file)
        print(f"文件 {idx + 1} 总结完毕")

    print("\n测试 classify_files:")
    result = classifier.classify_files(files)
    files = result["files"]
    categories = result["categories"]
    print("分类后的文件列表:")
    print(files)
    print("分类后的目录列表:")
    print(categories)

    print("\n测试 classify_file:")
    files[0] = classifier.classify_file(files[0], categories)
    print("分类后的文件:")
    print(files[0])

    print("\n测试 get_match_files:")
    print(classifier.get_match_files("研究生", files))


if __name__ == "__main__":
    main()