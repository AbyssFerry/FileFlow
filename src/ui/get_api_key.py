from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QApplication, QGraphicsDropShadowEffect
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor
from src.ui.uiprint import print

class GetAPIKey(QWidget):
    api_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("输入API Key")
        self.resize(520, 220)
        # 设置为模态窗口并禁用关闭按钮
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        # A风格主窗口背景
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e3e8ee);
                border-radius: 18px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(28)

        # 添加提示标签
        label = QLabel("请输入API Key:")
        label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-family: 'Microsoft YaHei';
                color: #222;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # 添加输入框
        self.api_input = QLineEdit()
        self.api_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                font-family: 'Microsoft YaHei';
                padding: 10px 14px;
                min-height: 44px;
                border-radius: 8px;
                border: 2px solid #b6c6e2;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 2.5px solid #1565c0;
                background: #f0f6ff;
            }
        """)
        self.api_input.returnPressed.connect(self.submit_api)
        layout.addWidget(self.api_input)

        # A风格按钮
        btn_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        submit_btn = QPushButton("确定")
        submit_btn.setFont(btn_font)
        submit_btn.setFixedHeight(48)
        submit_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 18px;
                border-radius: 10px;
                padding: 10px 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e0e7ef, stop:1 #b6c6e2);
                color: #222;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #c7d7ee, stop:1 #a4b8d8);
                color: #1565c0;
            }
            QPushButton:pressed {
                background: #b0b8c9;
                color: #0d47a1;
            }
        """)
        # 按钮阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(14)
        shadow.setColor(QColor(180, 190, 210, 120))
        shadow.setOffset(0, 3)
        submit_btn.setGraphicsEffect(shadow)

        submit_btn.clicked.connect(self.submit_api)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_api(self):
        api_key = self.api_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "提示", "请输入API Key")
            return
        
        print(f"API Key: {api_key}")
        self.api_submitted.emit(api_key)
        self.close()

    def closeEvent(self, event):
        if not self.api_input.text().strip():
            reply = QMessageBox.question(self, '确认', 
                                       "您确定要退出吗？\n如果不输入API Key，程序将无法继续。",
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
                QApplication.quit()
            else:
                event.ignore()
        else:
            event.accept()