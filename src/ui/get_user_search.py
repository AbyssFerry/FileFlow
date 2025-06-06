from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from show_target_files import ShowTargetFiles
from show_progress_bar import ShowProgressBar
from PyQt5.QtCore import QTimer

class GetUserSearch(QWidget):
    def __init__(self):
        super().__init__()
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
        keyword = self.input_line.text()
        print(f"用户输入的关键词：{keyword}")

        # 显示进度条窗口，模拟搜索过程
        self.progress_window = ShowProgressBar(self)
        self.progress_window.show()
        self.progress_window.start_progress("查询完成")

        # 等待进度条完成后再显示结果窗口（假设进度条500ms完成）
        QTimer.singleShot(600, self.show_results)

    def show_results(self):
        self.target_files_window = ShowTargetFiles()
        self.target_files_window.show()



