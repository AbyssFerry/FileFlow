import os
from parse_folder_path import parse_folder_path
import sys
from parser_file import parser_file 
from pack_search import pack_search
from src.storage.database import reset_database, fileShow, folderShow
# 临时关闭 stderr（不推荐长期使用）
sys.stderr = open(os.devnull, 'w')

large_data = r"D:\vs code\python\FileFlow\testdoc\large_test"
middle_data = r"D:\vs code\python\FileFlow\testdoc\middle_test"
small_data = r"D:\vs code\python\FileFlow\testdoc\small_test"
tiny_data = r"D:\vs code\python\FileFlow\testdoc\tiny_test"

if __name__ == "__main__":
    reset_database()
    print(fileShow(),folderShow())
    # 1
    print("====第一步：解析大数据目录====")
    flag = parse_folder_path(middle_data)
    if flag == 1:
        print("AC")
    # 2
    print("====第二步：归类文件====")
    pdf_newPath_and_reason =parser_file(r"D:\vs code\python\FileFlow\testdoc\addDoc\计算机与网络空间安全学院2023级考勤实施细则.pdf")
    print(pdf_newPath_and_reason)

    doc_newPath_and_reason = parser_file(r"D:\vs code\python\FileFlow\testdoc\addDoc\附件4：福建师范大学考场规则.doc")
    print(doc_newPath_and_reason)
    
    excel_newPath_and_reason = parser_file(r"D:\vs code\python\FileFlow\testdoc\addDoc\2024-2025学年第一学期通识教育必修课补考安排表.xlsx")
    print(excel_newPath_and_reason)
    # 3
    print("====第三步：搜索====")
    files = pack_search("关于宿舍的文件")
    print(files)