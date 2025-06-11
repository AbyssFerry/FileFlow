from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from src.ui.uiprint import print

class ShowMoveTarget(QWidget):
    def __init__(self, move_info=None):
        super().__init__()
        self.setWindowTitle("文件移动信息")
        self.resize(1500, 780)  # 窗口变为原来的3倍大
        
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        
        # 处理传入的移动信息，如果为None则使用默认值
        self.move_info = move_info or {
            "name": "未知文件",
            "new_absolute_path": "路径未指定",
            "reason_for_move": "原因未知"
        }
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 使用传入的信息创建标签，并设置自动换行，字体为微软雅黑18px
        label_style = "font-size: 18px; font-family: 'Microsoft YaHei'; font-weight: bold;"

        name_label = QLabel(f"文件名称:\n{self.move_info['name']}")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(label_style)
        name_label.setWordWrap(True)

        path_label = QLabel(f"新路径:\n{self.move_info['new_absolute_path']}")
        path_label.setAlignment(Qt.AlignCenter)
        path_label.setStyleSheet(label_style)
        path_label.setWordWrap(True)

        reason_label = QLabel(f"移动原因:\n{self.move_info['reason_for_move']}")
        reason_label.setAlignment(Qt.AlignCenter)
        reason_label.setStyleSheet(label_style)
        reason_label.setWordWrap(True)

        # 垂直居中布局
        layout.addStretch()
        layout.addWidget(name_label)
        layout.addWidget(path_label)
        layout.addWidget(reason_label)
        layout.addStretch()

        self.setLayout(layout)