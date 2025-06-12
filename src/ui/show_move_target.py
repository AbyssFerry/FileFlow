from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from src.ui.uiprint import print

class ShowMoveTarget(QWidget):
    def __init__(self, move_info=None):
        super().__init__()
        self.setWindowTitle("文件移动信息")
        self.resize(900, 600)  # 风格A推荐窗口大小

        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # 设置A风格主窗口背景色和圆角
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e3e8ee);
                border-radius: 24px;
            }
        """)

        # 处理传入的移动信息，如果为None则使用默认值
        self.move_info = move_info or {
            "name": "未知文件",
            "new_absolute_path": "路径未指定",
            "reason_for_move": "原因未知"
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(36)

        # A风格标题
        title_label = QLabel("文件移动结果")
        title_font = QFont("Microsoft YaHei", 32, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #222;
                letter-spacing: 8px;
                font-weight: bold;
                margin-bottom: 20px;
                text-shadow: 2px 2px 8px #e0e0e0;
            }
        """)
        layout.addWidget(title_label)

        # A风格内容标签
        label_font = QFont("Microsoft YaHei", 22)
        label_style = """
            QLabel {
                font-size: 22px;
                font-family: 'Microsoft YaHei';
                border: 2.5px dashed #b6c6e2;
                border-radius: 14px;
                padding: 36px;
                margin-bottom: 24px;
                background: #fafdff;
                color: #222;
            }
        """

        def create_shadow_label(text):
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(label_font)
            label.setStyleSheet(label_style)
            label.setWordWrap(True)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(12)
            shadow.setColor(QColor(180, 190, 210, 120))
            shadow.setOffset(0, 4)
            label.setGraphicsEffect(shadow)
            return label

        name_label = create_shadow_label(f"文件名称：\n{self.move_info['name']}")
        path_label = create_shadow_label(f"新路径：\n{self.move_info['new_absolute_path']}")
        reason_label = create_shadow_label(f"移动原因：\n{self.move_info['reason_for_move']}")

        layout.addStretch()
        layout.addWidget(name_label)
        layout.addWidget(path_label)
        layout.addWidget(reason_label)
        layout.addStretch()

        self.setLayout(layout)