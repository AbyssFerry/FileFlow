from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor
from src.ui.show_target_files import ShowTargetFiles
from src.controllers.pack_search import pack_search
from src.ui.uiprint import print

# 添加QThread子类替代Process
class SearchThread(QThread):
    result_ready = pyqtSignal(object)
    
    def __init__(self, keyword, api_key):
        super().__init__()
        self.keyword = keyword
        self.api_key = api_key
        
    def run(self):
        try:
            result = pack_search(self.keyword, self.api_key)
            self.result_ready.emit(result)
        except Exception as e:
            self.result_ready.emit({"error": str(e)})

class GetUserSearch(QWidget):
    closed = pyqtSignal()  # 新增

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.search_results = None
        # 替换Process为Thread
        self.search_thread = None
        self.setWindowTitle("查询文件")
        self.resize(900, 340)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e3e8ee);
                border-radius: 24px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(32)

        title_label = QLabel("文件查询")
        title_font = QFont("Microsoft YaHei", 32, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #222;
                letter-spacing: 8px;
                font-weight: bold;
                margin-bottom: 18px;
                text-shadow: 2px 2px 8px #e0e0e0;
            }
        """)
        self.layout.addWidget(title_label)

        self.label = QLabel("请输入目标文件关键词")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-family: 'Microsoft YaHei';
                color: #222;
            }
        """)
        self.layout.addWidget(self.label)

        self.h_layout = QHBoxLayout()

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("请输入关键词")
        self.input_line.setMinimumWidth(500)
        self.input_line.setStyleSheet("""
            QLineEdit {
                font-size: 20px;
                padding: 12px;
                min-height: 48px;
                font-family: 'Microsoft YaHei';
                border-radius: 10px;
                border: 2px solid #b6c6e2;
                background: #fafdff;
            }
            QLineEdit:focus {
                border: 2.5px solid #1565c0;
                background: #f0f6ff;
            }
        """)
        self.input_line.returnPressed.connect(self.search)

        btn_font = QFont("Microsoft YaHei", 20, QFont.Bold)
        self.search_btn = QPushButton("查找")
        self.search_btn.setFont(btn_font)
        self.search_btn.setFixedSize(140, 48)
        self.search_btn.setStyleSheet("""
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 20px;
                border-radius: 12px;
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
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(14)
        shadow.setColor(QColor(180, 190, 210, 120))
        shadow.setOffset(0, 3)
        self.search_btn.setGraphicsEffect(shadow)

        self.search_btn.clicked.connect(self.search)

        self.h_layout.addWidget(self.input_line)
        self.h_layout.addWidget(self.search_btn)

        self.layout.addLayout(self.h_layout)

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
        # 保留此方法以保持兼容性，但不再使用
        pass

    def search(self):
        try:
            if not self.API_KEY:
                raise ValueError("API Key未设置")

            keyword = self.input_line.text().strip()
            if not keyword:
                raise ValueError("请输入搜索关键词")

            print(f"用户输入的关键词：{keyword}")
            print(f"使用的API Key：{self.API_KEY}")

            self.input_line.hide()
            self.search_btn.hide()
            self.searching_label.show()
            self.label.setText("正在查找，请耐心等待")

            # 替换Process为QThread
            if self.search_thread and self.search_thread.isRunning():
                self.search_thread.terminate()
                self.search_thread.wait()

            self.search_thread = SearchThread(keyword, self.API_KEY)
            self.search_thread.result_ready.connect(self.on_result_ready)
            self.search_thread.start()

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"搜索时发生错误：{str(e)}")
            print(f"错误: {str(e)}")

    def on_result_ready(self, result):
        self.input_line.show()
        self.search_btn.show()
        self.searching_label.hide()
        self.label.setText("请输入目标文件关键词")

        if isinstance(result, dict) and "error" in result:
            QMessageBox.critical(self, "错误", f"搜索时发生错误：{result['error']}")
            return

        self.search_results = result
        QTimer.singleShot(600, self.show_results)

    def closeEvent(self, event):
        # 终止线程而非进程
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.terminate()
            self.search_thread.wait()
        print("查找窗口已关闭")
        self.closed.emit()
        event.accept()

    def show_results(self):
        if not self.search_results:
            QMessageBox.warning(self, "提示", "未找到相关文件")
            self.input_line.show()
            self.search_btn.show()
            self.searching_label.hide()
            self.label.setText("请输入目标文件关键词")
            return

        self.target_files_window = ShowTargetFiles(files=self.search_results)
        self.target_files_window.show()