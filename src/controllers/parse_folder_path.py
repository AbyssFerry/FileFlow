import os
import pandas as pd
from docx import Document
import pdfplumber  # 替换 PyPDF2
from datetime import datetime


def parse_folder_path(directory):
    file_info_list = []

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # 跳过子目录
        if os.path.isfile(file_path):
            # 获取文件基本信息
            file_info = {
                "name": filename,
                "absolute_path": os.path.abspath(file_path),
                "extension": os.path.splitext(filename)[1].lower(),
                "created_time": datetime.fromtimestamp(
                    os.path.getctime(file_path)
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "size_bytes": os.path.getsize(file_path),
                "content": ""
            }

            # 根据文件扩展名读取内容
            try:
                ext = file_info["extension"]

                if ext == '.txt':
                    # 读取文本文件
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_info["content"] = f.read()

                elif ext == '.pdf':
                    # 使用 pdfplumber 读取 PDF 文件
                    with pdfplumber.open(file_path) as pdf:
                        content = []
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text:  # 确保文本不为空
                                content.append(text)
                        file_info["content"] = "\n".join(content)

                elif ext in ('.xlsx', '.xls'):
                    # 读取Excel文件
                    df = pd.read_excel(file_path)
                    file_info["content"] = df.to_string()

                elif ext == '.docx':
                    # 读取Word文件
                    doc = Document(file_path)
                    content = []
                    for para in doc.paragraphs:
                        content.append(para.text)
                    file_info["content"] = "\n".join(content)

                else:
                    file_info["content"] = "<不支持的文件格式>"

            except Exception as e:
                file_info["content"] = f"<读取文件时出错: {str(e)}>"

            file_info_list.append(file_info)

    return file_info_list
"""
def interactive_test():
    
    print("\n" + "="*50)
    print("文件解析器测试工具")
    print("="*50)
    
    while True:
        # 1. 获取用户输入的目录路径
        test_dir = input("\n请输入要测试的目录路径（输入q退出）: ").strip()
        if test_dir.lower() == 'q':
            break
            
        # 2. 检查目录是否存在
        if not os.path.isdir(test_dir):
            print(f"错误：目录不存在 - {test_dir}")
            continue
            
        # 3. 执行文件解析
        print(f"\n正在解析目录: {test_dir}")
        try:
            results = parse_folder_path(test_dir)
            
            # 4. 显示解析结果统计
            print(f"\n解析完成！共找到 {len(results)} 个文件")
            print("="*50)
            
            # 5. 显示每个文件的解析详情
            for i, file_info in enumerate(results, 1):
                print(f"\n【文件{i}】")
                print(f"名称: {file_info['name']}")
                print(f"路径: {file_info['absolute_path']}")
                print(f"类型: {file_info['extension']}")
                print(f"创建时间: {file_info['created_time']}")
                print(f"大小: {file_info['size_bytes']} 字节")
                
                # 内容预览（只显示前100字符）
                content_preview = str(file_info['content'])[:100]
                if len(str(file_info['content'])) > 100:
                    content_preview += "..."
                print("内容预览:", content_preview)
                
        except Exception as e:
            print(f"解析过程中出错: {str(e)}")
            
    print("\n测试工具已退出")

if __name__ == "__main__":
    interactive_test()"""