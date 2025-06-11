from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from multiprocessing import Process, Queue
from src.ui.show_target_files import ShowTargetFiles
# from src.ui.show_progress_bar import ShowProgressBar  # 注释进度条导入
from src.controllers.pack_search import pack_search
from src.ui.uiprint import print
 
def process_search(keyword, api_key, queue):
    try:
        result = pack_search(keyword, api_key)
        queue.put(result)
    except Exception as e:
        queue.put({"error": str(e)})

class GetUserSearch(QWidget):
    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.search_results = None
        self.process = None
        self.queue = Queue()
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_process)
        self.setWindowTitle("查询文件")
        self.resize(800, 250)  # 增大窗口尺寸
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(40, 30, 40, 30)  # 增加边距
        self.layout.setSpacing(20)  # 增加间距

        self.label = QLabel("请输入目标文件关键词")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-family: 'Microsoft YaHei';
            }
        """)

        self.h_layout = QHBoxLayout()

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("请输入关键词")
        self.input_line.setMinimumWidth(500)  # 增加输入框宽度
        self.input_line.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 8px;
                min-height: 45px;
                font-family: 'Microsoft YaHei';
            }
        """)
        self.input_line.returnPressed.connect(self.search)

        self.search_btn = QPushButton("查找")
        self.search_btn.setFixedSize(120, 45)  # 设置按钮大小
        self.search_btn.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-family: 'Microsoft YaHei';
            }
        """)
        self.search_btn.clicked.connect(self.search)

        self.h_layout.addWidget(self.input_line)
        self.h_layout.addWidget(self.search_btn)

        self.layout.addWidget(self.label)
        self.layout.addLayout(self.h_layout)

        # 查找中提示
        self.searching_label = QLabel("正在查找，请耐心等待ο(=•ω＜=)ρ⌒☆")
        self.searching_label.setAlignment(Qt.AlignCenter)
        self.searching_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: #888;
                font-family: 'Microsoft YaHei';
            }
        """)
        self.searching_label.hide()
        self.layout.addWidget(self.searching_label)

        self.setLayout(self.layout)

    def check_process(self):
        if not self.queue.empty():
            result = self.queue.get()
            self.check_timer.stop()
            
            # 恢复输入框和按钮
            self.input_line.show()
            self.search_btn.show()
            self.searching_label.hide()
            self.label.setText("请输入目标文件关键词")

            if isinstance(result, dict) and "error" in result:
                QMessageBox.critical(self, "错误", f"搜索时发生错误：{result['error']}")
                return
                
            self.search_results = result
            # self.progress_window.start_progress("查询完成")  # 注释进度条更新
            QTimer.singleShot(600, self.show_results)

    def search(self):
        try:
            if not self.API_KEY:
                raise ValueError("API Key未设置")

            keyword = self.input_line.text().strip()
            if not keyword:
                raise ValueError("请输入搜索关键词")

            print(f"用户输入的关键词：{keyword}")
            print(f"使用的API Key：{self.API_KEY}")

            # 隐藏输入框和按钮，显示查找中提示
            self.input_line.hide()
            self.search_btn.hide()
            self.searching_label.show()
            self.label.setText("正在查找，请耐心等待ο(=•ω＜=)ρ⌒☆")

            # 显示进度条窗口
            # self.progress_window = ShowProgressBar(self)  # 注释进度条创建
            # self.progress_window.show()  # 注释进度条显示
            
            # 启动搜索进程
            if self.process and self.process.is_alive():
                self.process.terminate()
                
            self.process = Process(target=process_search, 
                                 args=(keyword, self.API_KEY, self.queue))
            self.process.start()
            self.check_timer.start(100)  # 每100ms检查一次结果

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索时发生错误：{str(e)}")
            print(f"错误: {str(e)}")

    def closeEvent(self, event):
        if self.process and self.process.is_alive():
            self.process.terminate()
        event.accept()

    def show_results(self):
        if not self.search_results:
            QMessageBox.warning(self, "提示", "未找到相关文件")
            # 恢复输入框和按钮
            self.input_line.show()
            self.search_btn.show()
            self.searching_label.hide()
            self.label.setText("请输入目标文件关键词")
            return
            
        # 创建结果窗口并传递搜索结果
        self.target_files_window = ShowTargetFiles(files=self.search_results)
        self.target_files_window.show()