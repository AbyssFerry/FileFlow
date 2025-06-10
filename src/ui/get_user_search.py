from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from src.ui.show_target_files import ShowTargetFiles
from src.ui.show_progress_bar import ShowProgressBar
from PyQt5.QtCore import QTimer
from src.controllers.pack_search import pack_search

class GetUserSearch(QWidget):
    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.search_results = None  # 添加存储搜索结果的变量
        self.setWindowTitle("查询文件")
        self.resize(480, 160)  
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("请输入目标文件关键词")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px;")  

        h_layout = QHBoxLayout()

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("请输入关键词")
        self.input_line.setMinimumWidth(320)
        self.input_line.setStyleSheet("font-size: 16px;")  
        self.input_line.returnPressed.connect(self.search)

        search_btn = QPushButton("查找")
        search_btn.clicked.connect(self.search)
        search_btn.setFixedWidth(90)
        search_btn.setStyleSheet("font-size: 16px;")  

        h_layout.addWidget(self.input_line)
        h_layout.addWidget(search_btn)

        layout.addWidget(label)
        layout.addLayout(h_layout)

        self.setLayout(layout)

    def search(self):
        try:
            if not self.API_KEY:
                raise ValueError("API Key未设置")

            keyword = self.input_line.text().strip()
            if not keyword:
                raise ValueError("请输入搜索关键词")

            # 保存搜索结果
            self.search_results = pack_search(keyword, self.API_KEY)
            print(f"用户输入的关键词：{keyword}")
            print(f"使用的API Key：{self.API_KEY}")

            # 显示进度条窗口
            self.progress_window = ShowProgressBar(self)
            self.progress_window.show()
            self.progress_window.start_progress("查询完成")

            # 等待进度条完成后显示结果
            QTimer.singleShot(600, self.show_results)

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索时发生错误：{str(e)}")
            print(f"错误: {str(e)}")

    def show_results(self):
        if not self.search_results:
            QMessageBox.warning(self, "提示", "未找到相关文件")
            return
            
        # 创建结果窗口并传递搜索结果
        self.target_files_window = ShowTargetFiles(files=self.search_results)
        self.target_files_window.show()


