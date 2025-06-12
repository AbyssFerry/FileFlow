from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox, QLabel, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from src.ui.get_init_folder import GetInitFolder
from src.ui.get_add_file import GetAddFile
from src.ui.get_user_search import GetUserSearch
from src.ui.get_api_key import GetAPIKey
from src.ui.uiprint import print
from src.storage.database import is_file_table_empty
from src.storage.database import reset_database

class GetUserChoice(QWidget):
    def __init__(self):
        super().__init__()
        self.API_KEY = None
        self.child_window_opened = False
        self.setWindowTitle("请选择操作")
        self.resize(900, 700)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e3e8ee);
                border-radius: 24px;
            }
        """)

        self.init_ui()
        self.hide()
        self.show_api_input()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(50)

        btn_font = QFont("Microsoft YaHei", 26, QFont.Bold)
        btn_style = """
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 26px;
                border-radius: 16px;
                padding: 22px 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e0e7ef, stop:1 #b6c6e2);
                color: #222;
                border: none;
                box-shadow: 0px 4px 16px rgba(0,0,0,0.08);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #c7d7ee, stop:1 #a4b8d8);
                color: #1565c0;
            }
            QPushButton:pressed {
                background: #b0b8c9;
                color: #0d47a1;
            }
        """

        self.btns = {}

        def create_button(text, slot, key=None):
            btn_container = QHBoxLayout()
            btn = QPushButton(text)
            btn.setFont(btn_font)
            btn.setFixedSize(420, 80)
            btn.setStyleSheet(btn_style)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(18)
            shadow.setColor(QColor(180, 190, 210, 120))
            shadow.setOffset(0, 6)
            btn.setGraphicsEffect(shadow)
            btn.clicked.connect(slot)
            btn_container.addStretch()
            btn_container.addWidget(btn)
            btn_container.addStretch()
            main_layout.addLayout(btn_container)
            if key:
                self.btns[key] = btn

        title_label = QLabel("FILE-FLOW")
        title_font = QFont("Microsoft YaHei", 44, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #222;
                letter-spacing: 10px;
                font-weight: bold;
                margin-bottom: 40px;
                text-shadow: 2px 2px 8px #e0e0e0;
            }
        """)
        main_layout.addWidget(title_label)

        create_button("重置数据库", self.reset_database_and_restart)
        create_button("初始化文件库", self.open_init_folder, key="init")
        create_button("添加文件", self.open_add_file, key="add")
        create_button("查询文件", self.open_search, key="search")
        create_button("退出", self.try_quit, key="quit")

        self.setLayout(main_layout)

    def reset_database_and_restart(self):
        if self.child_window_opened:
            QMessageBox.warning(self, "警告", "请先关闭当前子窗口后再进行其他操作")
            return
        reply = QMessageBox.question(self, "重置数据库", "确定要重置数据库吗？此操作会清空所有数据且无法恢复！",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reset_database()
            QMessageBox.information(self, "提示", "数据库已重置，请重新初始化文件库。")

    def show_api_input(self):
        self.api_window = GetAPIKey()
        self.api_window.api_submitted.connect(self.on_api_received)
        self.api_window.show()

    def on_api_received(self, api_key):
        if api_key:
            print("API Key 已接收:", api_key)
            self.API_KEY = api_key
            self.show()
        else:
            print("未接收到API Key")
            self.close()

    def open_init_folder(self):
        if self.child_window_opened:
            QMessageBox.warning(self, "警告", "请先关闭当前子窗口后再进行其他操作")
            return
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        self.init_window = GetInitFolder(API_KEY=self.API_KEY)
        self.init_window.folder_dropped.connect(self.handle_folder_dropped)
        self.init_window.closed.connect(self.child_window_closed)  # 用自定义信号
        self.child_window_opened = True
        self.init_window.show()

    def handle_folder_dropped(self, folder_path):
        pass

    def open_add_file(self):
        if self.child_window_opened:
            QMessageBox.warning(self, "警告", "请先关闭当前子窗口后再进行其他操作")
            return
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        if is_file_table_empty():
            QMessageBox.warning(self, "警告", "请先初始化文件库")
            return
        self.add_window = GetAddFile(API_KEY=self.API_KEY)
        self.add_window.file_dropped.connect(self.handle_file_dropped)
        self.add_window.closed.connect(self.child_window_closed)  # 用自定义信号
        self.child_window_opened = True
        self.add_window.show()

    def handle_file_dropped(self, file_path):
        pass

    def open_search(self):
        if self.child_window_opened:
            QMessageBox.warning(self, "警告", "请先关闭当前子窗口后再进行其他操作")
            return
        if not self.API_KEY:
            print("API Key未设置")
            QMessageBox.warning(self, "警告", "API Key未设置")
            return
        if is_file_table_empty():
            QMessageBox.warning(self, "警告", "请先初始化文件库")
            return
        self.search_window = GetUserSearch(API_KEY=self.API_KEY)
        self.search_window.closed.connect(self.child_window_closed)  # 用自定义信号
        self.child_window_opened = True
        self.search_window.show()

    def child_window_closed(self):
        self.child_window_opened = False

    def try_quit(self):
        if self.child_window_opened:
            QMessageBox.warning(self, "警告", "请先关闭当前子窗口后再进行其他操作")
            return
        self.close()

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