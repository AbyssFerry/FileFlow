from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
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

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.setWindowTitle("拖入文件")
        self.setAcceptDrops(True)
        self.resize(800, 600)  # 增大窗口尺寸
        self.init_ui()
        self.process = None
        self.queue = Queue()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_process)
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)  # 增加边距
        
        self.label = QLabel("请将文件拖入此区域")
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
                font-size: 16px;
                font-family: 'Microsoft YaHei';
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setVisible(False)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def check_process(self):
        if not self.queue.empty():
            result = self.queue.get()
            self.timer.stop()
            
            if isinstance(result, dict) and "error" in result:
                QMessageBox.critical(self, "错误", f"处理文件时发生错误：{result['error']}")
                return
                
            if not result:
                QMessageBox.warning(self, "警告", "文件解析失败")
                return
                
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
            urls = event.mimeData().urls()
            if not urls:
                return
                
            file_path = urls[0].toLocalFile()
            if not os.path.isfile(file_path):
                self.label.setText("请拖入一个有效的文件")
                return

            self.label.setText(f"正在处理文件：\n{file_path}\n请稍候...")
            
            if not self.API_KEY:
                raise ValueError("API Key未设置")

            print(f"[终端输出] 拖入的文件路径为：{file_path}")
            print(f"使用的API Key为：{self.API_KEY}")
            
            # 启动新进程处理文件
            if self.process and self.process.is_alive():
                self.process.terminate()
                
            self.process = Process(target=process_file, 
                                 args=(file_path, self.API_KEY, self.queue))
            self.process.start()
            self.timer.start(100)  # 每100ms检查一次结果
            
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
        if self.process and self.process.is_alive():
            self.process.terminate()
        if hasattr(self, 'move_info_window'):
            self.move_info_window.close()
        event.accept()






