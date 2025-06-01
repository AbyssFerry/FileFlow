#进度条

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PyQt5.QtCore import Qt


class ProgressBarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("进度条")
        self.resize(300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("进度：")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.confirm_button = QPushButton("确定")
        self.confirm_button.setVisible(False)
        self.confirm_button.clicked.connect(self.close)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.confirm_button)
        self.setLayout(layout)

    def start_progress(self):
        self.show()
        self.progress_bar.setValue(0)
        self.label.setText("进度：")
        self.confirm_button.setVisible(False)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value >= 100:
            self.label.setText("完成！")
            self.confirm_button.setVisible(True)
            self.confirm_button.repaint()
            self.repaint()
        else:
            self.label.setText(f"进度：{value}%")

