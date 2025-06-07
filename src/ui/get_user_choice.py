#让用户选择拖入操作还是查询操作

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from get_init_folder import GetInitFolder
from get_add_file import GetAddFile
from get_user_search import GetUserSearch
from show_progress_bar import ShowProgressBar

class GetUserChoice(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("请选择操作")
        self.resize(400, 320)  # 稍微加高一点适配三个按钮
        self.init_ui()
        self.progress_window = None  

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(30)

        font = QFont()
        font.setPointSize(15)

        def create_button(text, slot):
            btn_container = QHBoxLayout()
            btn = QPushButton(text)
            btn.setFont(font)
            btn.setFixedSize(250, 55)
            btn.clicked.connect(slot)
            btn_container.addStretch()
            btn_container.addWidget(btn)
            btn_container.addStretch()
            main_layout.addLayout(btn_container)

        create_button("初始化文件库", self.open_init_folder)
        create_button("添加文件", self.open_add_file)
        create_button("查询文件", self.open_search)

        self.setLayout(main_layout)

    def open_init_folder(self):
        self.init_window = GetInitFolder()
        self.init_window.folder_dropped.connect(self.handle_folder_dropped)
        self.init_window.show()

    def handle_folder_dropped(self, folder_path):
        self.progress_window = ShowProgressBar(self.init_window)
        self.progress_window.show()
        self.progress_window.start_progress("文件目录整理成功")

    def open_add_file(self):
        self.add_window = GetAddFile()
        self.add_window.file_dropped.connect(self.handle_file_dropped)
        self.add_window.show()

    def handle_file_dropped(self, file_path):
        self.progress_window = ShowProgressBar(self.add_window)
        self.progress_window.show()
        self.progress_window.start_progress("文件整理完成")

    def open_search(self):
        self.search_window = GetUserSearch()
        self.search_window.show()



