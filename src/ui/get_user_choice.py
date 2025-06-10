from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from src.ui.get_init_folder import GetInitFolder
from src.ui.get_add_file import GetAddFile
from src.ui.get_user_search import GetUserSearch
from src.ui.show_progress_bar import ShowProgressBar
from src.ui.get_api_key import GetAPIKey

class GetUserChoice(QWidget):
    def __init__(self):
        super().__init__()
        self.API_KEY = None
        self.setWindowTitle("请选择操作")
        self.resize(400, 320)
        self.progress_window = None
        
        # 完全初始化界面但不显示
        self.init_ui()
        self.hide()
        
        # 显示API输入窗口
        self.show_api_input()

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

    def show_api_input(self):
        self.api_window = GetAPIKey()
        self.api_window.api_submitted.connect(self.on_api_received)
        self.api_window.show()

    def on_api_received(self, api_key):
        if api_key:
            print("API Key 已接收:", api_key)
            self.API_KEY = api_key
            self.show()  # 只有在成功接收到API后才显示主窗口
        else:
            print("未接收到API Key")
            self.close()

    def open_init_folder(self):
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        self.init_window = GetInitFolder(API_KEY=self.API_KEY)
        self.init_window.folder_dropped.connect(self.handle_folder_dropped)
        self.init_window.show()

    def handle_folder_dropped(self, folder_path):
        self.progress_window = ShowProgressBar(self.init_window)
        self.progress_window.show()
        self.progress_window.start_progress("文件目录整理成功")

    def open_add_file(self):
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        self.add_window = GetAddFile(API_KEY=self.API_KEY)  # 修改这里，传入API_KEY
        self.add_window.file_dropped.connect(self.handle_file_dropped)
        self.add_window.show()

    def handle_file_dropped(self, file_path):
        self.progress_window = ShowProgressBar(self.add_window)
        self.progress_window.show()
        self.progress_window.start_progress("文件整理完成")

    def open_search(self):
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        self.search_window = GetUserSearch(API_KEY=self.API_KEY)  # 修改这里，传入API_KEY
        self.search_window.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认',
                                   "确定要退出程序吗？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            QApplication.quit()
        else:
            event.ignore()