from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import os
import traceback
from src.controllers.parse_folder_path import parse_folder_path
from src.ui.uiprint import print

class ParseFolderThread(QThread):
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    log_signal = pyqtSignal(str)  # 新增日志信号

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

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.is_processing = False
        self.parse_thread = None
        self.setWindowTitle("拖入文件夹")
        self.setAcceptDrops(True)
        self.resize(800, 600)  # 增大窗口尺寸
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)  # 增加边距
        
        self.label = QLabel("请将文件夹拖入此区域")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                border: 3px dashed #aaa;
                font-size: 24px;
                padding: 40px;
                font-family: 'Microsoft YaHei';
            }
        """)
        layout.addWidget(self.label)

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFixedHeight(50)  # 增大按钮高度
        self.close_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-family: 'Microsoft YaHei', '微软雅黑';
                padding: 5px 15px;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setVisible(False)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

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
                    print("\n[开始] 准备处理文件夹...")
                    self.is_processing = True
                    self.label.setText(f"正在处理文件夹：\n{folder_path}\n请稍候...")
                    
                    self.parse_thread = ParseFolderThread(folder_path, self.API_KEY)
                    self.parse_thread.log_signal.connect(print)  # 连接日志信号到窗口print
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

    def on_parse_error(self, error_msg):
        self.is_processing = False
        print(f"处理出错：{error_msg}")
        self.label.setText(f"处理失败：{error_msg}")

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)

    def closeEvent(self, event):
        try:
            print("[关闭] 窗口正在关闭...")
            if self.parse_thread and self.parse_thread.isRunning():
                print("[关闭] 正在停止线程...")
                self.parse_thread.terminate()
                self.parse_thread.wait()
                print("[关闭] 线程已停止")
            event.accept()
        except Exception as e:
            error_info = traceback.format_exc()
            print(f"[关闭错误]\n{error_info}")
            event.accept()