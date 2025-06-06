#拖入文件目录

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
import os

class GetInitFolder(QWidget):
    folder_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖入文件夹")
        self.setAcceptDrops(True)
        self.resize(600, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("请将文件夹拖入此区域")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; font-size: 18px; padding: 20px;")
        layout.addWidget(self.label)

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFixedHeight(35)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setVisible(False)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            folder_path = urls[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.label.setText(f"已选择文件夹：\n{folder_path}")
                print(f"[终端输出] 拖入的文件夹路径为：{folder_path}")
                self.folder_dropped.emit(folder_path)
            else:
                self.label.setText("请拖入一个有效的文件夹")

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)





