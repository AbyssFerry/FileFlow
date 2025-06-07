from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ShowMoveTarget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件移动信息")
        self.resize(400, 200)  # 窗口大小

        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        new_path = r"D:\desktop\test"
        reason = "因为这个文件和测试有关"

        label_path = QLabel(f"文件新路径:\n{new_path}")
        label_path.setAlignment(Qt.AlignCenter)
        label_path.setStyleSheet("font-size: 18px; font-weight: bold;")

        label_reason = QLabel(f"放置原因:\n{reason}")
        label_reason.setAlignment(Qt.AlignCenter)
        label_reason.setStyleSheet("font-size: 18px; font-weight: bold;")

        # 上弹性间距，内容， 下弹性间距，保证内容垂直居中
        layout.addStretch()
        layout.addWidget(label_path)
        layout.addWidget(label_reason)
        layout.addStretch()

        self.setLayout(layout)





