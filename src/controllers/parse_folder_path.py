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