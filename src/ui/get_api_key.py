from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from src.ui.uiprint import print

class GetAPIKey(QWidget):
    api_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("输入API Key")
        self.resize(400, 150)
        # 设置为模态窗口并禁用关闭按钮
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)

        # 添加提示标签
        label = QLabel("请输入API Key:")
        label.setFont(QFont(None, 10))
        layout.addWidget(label)

        # 添加输入框
        self.api_input = QLineEdit()
        self.api_input.setFont(QFont(None, 10))
        self.api_input.returnPressed.connect(self.submit_api)
        layout.addWidget(self.api_input)

        # 添加确认按钮
        submit_btn = QPushButton("确定")
        submit_btn.setFont(QFont(None, 10))
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