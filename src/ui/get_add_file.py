#拖入单个文件

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
import os
from show_move_target import ShowMoveTarget

class GetAddFile(QWidget):
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖入文件")
        self.setAcceptDrops(True)
        self.resize(600, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("请将文件拖入此区域")
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
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.label.setText(f"已选择文件：\n{file_path}")
                print(f"[终端输出] 拖入的文件路径为：{file_path}")
                self.file_dropped.emit(file_path)

                # 弹出文件移动信息窗口，置于进度条窗口之下，拖入窗口之上
                self.move_info_window = ShowMoveTarget()
                self.move_info_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)
                self.move_info_window.show()
                self.move_info_window.raise_()

                # 显示关闭按钮
                self.close_btn.setVisible(True)

            else:
                self.label.setText("请拖入一个有效的文件")

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)








