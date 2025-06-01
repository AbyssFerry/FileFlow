from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class UserSearchWidget(QWidget):
    search_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("查询文件")
        self.resize(300, 150)

        layout = QVBoxLayout()
        label = QLabel("请输入查询内容：")
        self.input_line = QLineEdit()
        btn_submit = QPushButton("查询")

        btn_submit.clicked.connect(self.submit_search)

        layout.addWidget(label)
        layout.addWidget(self.input_line)
        layout.addWidget(btn_submit)

        self.setLayout(layout)

    def submit_search(self):
        text = self.input_line.text().strip()
        if text:
            self.search_submitted.emit(text)

