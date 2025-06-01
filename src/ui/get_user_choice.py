#让用户选择拖入操作还是查询操作

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal

class UserChoiceWidget(QWidget):
    choice_made = pyqtSignal(str)  # 'drop' 或 'search'

    def __init__(self):
        super().__init__()
        self.setWindowTitle("请选择操作")
        self.resize(300, 150)

        layout = QVBoxLayout()
        label = QLabel("请选择操作：")
        layout.addWidget(label)

        btn_drop = QPushButton("拖入文件目录或文件")
        btn_search = QPushButton("查询文件")

        btn_drop.clicked.connect(lambda: self.emit_choice("drop"))
        btn_search.clicked.connect(lambda: self.emit_choice("search"))

        layout.addWidget(btn_drop)
        layout.addWidget(btn_search)

        self.setLayout(layout)

    def emit_choice(self, choice):
        self.choice_made.emit(choice)
        self.close()


