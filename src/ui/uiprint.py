from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
import sys

class PrintWindow(QWidget):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            instance = super(PrintWindow, cls).__new__(cls)
            super(PrintWindow, instance).__init__()
            cls._instance = instance
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.setup_ui()
            
    def setup_ui(self):
        self.setWindowTitle("控制台输出")
        self.resize(600, 400)
        
        layout = QVBoxLayout()
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 5px;
            }
        """)
        
        layout.addWidget(self.text_area)
        self.setLayout(layout)
        
        # 将窗口置于右上角
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 50, 50)

    def append_text(self, text):
        self.text_area.append(str(text))
        scrollbar = self.text_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

def print(*args, sep=' ', end='\n'):
    """在弹窗中显示文本"""
    # 确保有QApplication实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 获取打印窗口实例
    window = PrintWindow()
    if not window.isVisible():
        window.show()
    
    # 构造并显示文本
    text = sep.join(str(arg) for arg in args) + end
    window.append_text(text.rstrip())