from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import os
from src.ui.show_move_target import ShowMoveTarget
from src.controllers.parser_file import parser_file

class GetAddFile(QWidget):
    file_dropped = pyqtSignal(str)

    def __init__(self, API_KEY=None):
        super().__init__()
        self.API_KEY = API_KEY
        self.setWindowTitle("拖入文件")
        self.setAcceptDrops(True)
        self.resize(600, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("请将文件拖入此区域")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 2px dashed #aaa; font-size: 18px; padding: 20px;")
        layout.addWidget(self.label)

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFixedHeight(35)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.setVisible(False)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

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

            self.label.setText(f"已选择文件：\n{file_path}")
            
            # 验证API Key
            if not self.API_KEY:
                raise ValueError("API Key未设置")

            # 获取文件解析结果
            newPath_and_reason = parser_file(file_path, self.API_KEY)
            print(f"[终端输出] 拖入的文件路径为：{file_path}")
            print(f"使用的API Key为：{self.API_KEY}")
            
            if not newPath_and_reason:
                raise ValueError("文件解析失败")

            # 将解析结果传递给移动信息窗口
            self.move_info_window = ShowMoveTarget(newPath_and_reason)
            self.move_info_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.move_info_window.show()
            self.move_info_window.raise_()
            
            self.file_dropped.emit(file_path)
            self.close_btn.setVisible(True)

        except ValueError as e:
            QMessageBox.warning(self, "警告", str(e))
            print(f"错误: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理文件时发生错误：{str(e)}")
            print(f"错误: {str(e)}")

    def set_close_buttons_visible(self, visible: bool):
        self.close_btn.setVisible(visible)

    def closeEvent(self, event):
        # 关闭时同时关闭移动信息窗口
        if hasattr(self, 'move_info_window'):
            self.move_info_window.close()
        event.accept()






