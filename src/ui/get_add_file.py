from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QFont, QColor
import os
from src.ui.show_move_target import ShowMoveTarget
from src.controllers.parser_file import parser_file
from src.ui.uiprint import print

# 添加QThread子类替代Process
class FileProcessThread(QThread):
    result_ready = pyqtSignal(object)
    
    def __init__(self, file_path, api_key):
        super().__init__()
        self.file_path = file_path
        self.api_key = api_key
        
    def run(self):
        try:
            result = parser_file(self.file_path, self.api_key)
            self.result_ready.emit(result)
        except Exception as e:
            self.result_ready.emit({"error": str(e)})

class GetAddFile(QWidget):
    file_dropped = pyqtSignal(str)
    closed = pyqtSignal()  # 新增

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.setWindowTitle("拖入文件")
        self.setAcceptDrops(True)
        self.resize(900, 650)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e3e8ee);
                border-radius: 24px;
            }
        """)
        self.init_ui()
        # 替换Process为Thread
        self.file_thread = None
        self.is_processing = False

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(40)

        title_label = QLabel("文件添加")
        title_font = QFont("Microsoft YaHei", 36, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #222;
                letter-spacing: 8px;
                font-weight: bold;
                margin-bottom: 30px;
                text-shadow: 2px 2px 8px #e0e0e0;
            }
        """)
        layout.addWidget(title_label)

        self.label = QLabel("请将文件拖入此区域")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(180)
        self.label.setStyleSheet("""
            QLabel {
                border: 3px dashed #aaa;
                font-size: 28px;
                padding: 56px;
                font-family: 'Microsoft YaHei';
                background: #f8fafc;
                border-radius: 20px;
                color: #222;
            }
        """)
        layout.addWidget(self.label)

        btn_font = QFont("Microsoft YaHei", 22, QFont.Bold)
        btn_style = """
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 22px;
                border-radius: 12px;
                padding: 16px 0;
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
        """

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFont(btn_font)
        self.close_btn.setFixedSize(220, 56)
        self.close_btn.setStyleSheet(btn_style)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(180, 190, 210, 120))
        shadow.setOffset(0, 4)
        self.close_btn.setGraphicsEffect(shadow)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setVisible(False)
        layout.addWidget(self.close_btn, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def setEnabledClose(self, enabled: bool):
        if not enabled:
            self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        else:
            self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.show()

    def check_process(self):
        # 保留此方法以保持兼容性，但不再使用
        pass

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        try:
            if self.is_processing:
                return

            urls = event.mimeData().urls()
            if not urls:
                return

            file_path = urls[0].toLocalFile()
            if not os.path.isfile(file_path):
                self.label.setText("请拖入一个有效的文件")
                return

            self.label.setText(f"正在处理文件：\n{file_path}\n请稍候...")
            self.is_processing = True
            self.setEnabledClose(False)

            if not self.API_KEY:
                raise ValueError("API Key未设置")

            print(f"[终端输出] 拖入的文件路径为：{file_path}")
            print(f"使用的API Key为：{self.API_KEY}")

            # 替换Process为QThread
            if self.file_thread and self.file_thread.isRunning():
                self.file_thread.terminate()
                self.file_thread.wait()

            self.file_thread = FileProcessThread(file_path, self.API_KEY)
            self.file_thread.result_ready.connect(self.on_result_ready)
            self.file_thread.start()

            self.file_dropped.emit(file_path)

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
            self.is_processing = False
            self.setEnabledClose(True)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理文件时发生错误：{str(e)}")
            print(f"错误: {str(e)}")
            self.is_processing = False
            self.setEnabledClose(True)

    def on_result_ready(self, result):
        self.is_processing = False
        self.setEnabledClose(True)

        if isinstance(result, dict) and "error" in result:
            self.label.setText(f"处理文件时发生错误：{result['error']}")
            return

        if not result:
            self.label.setText("文件解析失败")
            return

        self.label.setText("文件添加成功！")

        self.move_info_window = ShowMoveTarget(result)
        self.move_info_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.move_info_window.show()
        self.move_info_window.raise_()
        self.close_btn.setVisible(True)

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)

    def closeEvent(self, event):
        if self.is_processing:
            event.ignore()
            return
        # 终止线程而非进程
        if self.file_thread and self.file_thread.isRunning():
            self.file_thread.terminate()
            self.file_thread.wait()
        if hasattr(self, 'move_info_window'):
            self.move_info_window.close()
        print("文件拖入窗口已关闭")
        self.closed.emit()
        event.accept()