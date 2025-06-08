#进度条

from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

class ShowProgressBar(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("进度条")
        self.resize(400, 150)

        # 最高置顶窗口
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.addStretch()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.layout.addWidget(self.progress)

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        self.layout.addStretch()

        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        self.close_button.hide()
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def start_progress(self, success_message):
        self.progress.setValue(50)
        print(success_message)

        QTimer.singleShot(500, self.complete_progress)

        self.close_button.hide()
        if self.parent_window:
            self.parent_window.setWindowFlag(Qt.WindowCloseButtonHint, False)
            self.parent_window.setWindowFlags(self.parent_window.windowFlags())
            self.parent_window.show()

    def complete_progress(self):
        self.progress.setValue(100)
        self.label.setText("成功了！O(∩_∩)O")

        self.close_button.show()
        if self.parent_window:
            self.parent_window.setWindowFlag(Qt.WindowCloseButtonHint, True)
            self.parent_window.setWindowFlags(self.parent_window.windowFlags())
            self.parent_window.show()





