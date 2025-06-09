import os
from parse_folder_path import parse_folder_path
import sys
from parser_file import parser_file 
from pack_search import pack_search
from src.storage.database import reset_database, fileShow, folderShow
# 临时关闭 stderr（不推荐长期使用）
#sys.stderr = open(os.devnull, 'w')




if __name__ == "__main__":
    reset_database()
    print(fileShow(),folderShow())
    # 1
    flag = parse_folder_path(r"D:\file-flow\src\controllers\exe")
    if flag == 1:
        print("AC")
    # 2
    pdf_newPath_and_reason =parser_file(r"D:\file-flow\src\controllers\example\校内模拟赛报名指南.pdf")
    print(pdf_newPath_and_reason)

    doc_newPath_and_reason = parser_file(r"D:\file-flow\src\controllers\example\学校寒假实践报告补充通知.doc")
    print(doc_newPath_and_reason)
    
    excel_newPath_and_reason = parser_file(r"D:\file-flow\src\controllers\example\学院中国国际大学生创新大赛2024项目摸底表.xlsx")
    print(excel_newPath_and_reason)
    # 3
    files = pack_search("关于奖学金的文件")
    print(files)