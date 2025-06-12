from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
import os
from multiprocessing import Process, Queue
from src.ui.show_move_target import ShowMoveTarget
from src.controllers.parser_file import parser_file
from src.ui.uiprint import print

def process_file(file_path, api_key, queue):
    try:
        result = parser_file(file_path, api_key)
        queue.put(result)
    except Exception as e:
        queue.put({"error": str(e)})

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
        self.process = None
        self.queue = Queue()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_process)
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
        if not self.queue.empty():
            result = self.queue.get()
            self.timer.stop()
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

            if self.process and self.process.is_alive():
                self.process.terminate()

            self.process = Process(target=process_file,
                                 args=(file_path, self.API_KEY, self.queue))
            self.process.start()
            self.timer.start(100)

            self.file_dropped.emit(file_path)

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理文件时发生错误：{str(e)}")
            print(f"错误: {str(e)}")

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)

    def closeEvent(self, event):
        if self.is_processing:
            event.ignore()
            return
        if self.process and self.process.is_alive():
            self.process.terminate()
        if hasattr(self, 'move_info_window'):
            self.move_info_window.close()
        print("文件拖入窗口已关闭")
        self.closed.emit()  # 关键：关闭时通知主窗口
        event.accept()