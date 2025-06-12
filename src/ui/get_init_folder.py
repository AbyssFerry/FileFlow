from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import os
import traceback
from src.controllers.parse_folder_path import parse_folder_path
from src.ui.uiprint import print

class ParseFolderThread(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    log_signal = pyqtSignal(str)

    def __init__(self, folder_path, api_key):
        super().__init__()
        self.folder_path = folder_path
        self.api_key = api_key

    def run(self):
        try:
            self.log_signal.emit("[线程] 开始执行文件夹解析...")
            result = parse_folder_path(self.folder_path, self.api_key)
            self.log_signal.emit("[线程] 解析完成")
            self.finished.emit(result)
        except Exception as e:
            error_info = traceback.format_exc()
            self.log_signal.emit(f"[线程错误]\n{error_info}")
            self.error.emit(str(e))

class GetInitFolder(QWidget):
    folder_dropped = pyqtSignal(str)
    closed = pyqtSignal()  # 新增

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.is_processing = False
        self.parse_thread = None
        self.setWindowTitle("拖入文件夹")
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

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(40)

        title_label = QLabel("文件夹初始化")
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

        self.label = QLabel("请将文件夹拖入此区域")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setMinimumHeight(220)
        self.label.setStyleSheet("""
            QLabel {
                border: 3px dashed #aaa;
                font-size: 28px;
                padding: 64px;
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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        try:
            if self.is_processing:
                return

            urls = event.mimeData().urls()
            if urls:
                folder_path = urls[0].toLocalFile()
                if os.path.isdir(folder_path):
                    subdirs = [f for f in os.listdir(folder_path)
                               if os.path.isdir(os.path.join(folder_path, f))]
                    if subdirs:
                        QMessageBox.warning(
                            self,
                            "子目录存在",
                            "检测到该目录下还有子文件夹，请将所有子目录下的文件移到当前目录后再拖入！"
                        )
                        self.label.setText("请将所有子目录下的文件移到当前目录后再拖入！")
                        return

                    print("\n[开始] 准备处理文件夹...")
                    self.is_processing = True
                    self.label.setText(f"正在处理文件夹：\n{folder_path}\n请稍候...")
                    self.setEnabledClose(False)

                    self.parse_thread = ParseFolderThread(folder_path, self.API_KEY)
                    self.parse_thread.log_signal.connect(print)
                    self.parse_thread.finished.connect(self.on_parse_finished)
                    self.parse_thread.error.connect(self.on_parse_error)
                    print("[线程] 正在启动线程...")
                    self.parse_thread.start()
                    print("[线程] 线程已启动")

                    self.folder_dropped.emit(folder_path)
                else:
                    self.label.setText("请拖入一个有效的文件夹")
        except Exception as e:
            error_info = traceback.format_exc()
            print(f"[主线程错误]\n{error_info}")
            self.label.setText(f"发生错误：{str(e)}")

    def on_parse_finished(self, result):
        self.is_processing = False
        self.label.setText("处理完成！" if result else "处理失败，请检查控制台输出")
        self.setEnabledClose(True)

    def on_parse_error(self, error_msg):
        self.is_processing = False
        print(f"处理出错：{error_msg}")
        self.label.setText(f"处理失败：{error_msg}")
        self.setEnabledClose(True)

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)

    def closeEvent(self, event):
        try:
            print("文件目录拖入窗口已关闭")
            if self.parse_thread and self.parse_thread.isRunning():
                print("[关闭] 正在停止线程...")
                self.parse_thread.terminate()
                self.parse_thread.wait()
                print("[关闭] 线程已停止")
            self.closed.emit()  # 关键：关闭时通知主窗口
            event.accept()
        except Exception as e:
            error_info = traceback.format_exc()
            print(f"[关闭错误]\n{error_info}")
            self.closed.emit()
            event.accept()