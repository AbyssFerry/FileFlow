from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import sys
import os
import traceback
import threading

# 设置高分屏缩放
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

def _safe_stderr(*args, **kwargs):
    # 只向标准错误输出，避免递归调用uiprint.print
    msg = " ".join(str(a) for a in args)
    sys.__stderr__.write(msg + kwargs.get("end", "\n"))
    sys.__stderr__.flush()

class PrintWindow(QWidget):
    _instance = None
    _lock = False

    def __new__(cls):
        if cls._instance is None and not cls._lock:
            try:
                cls._lock = True
                instance = super(PrintWindow, cls).__new__(cls)
                super(PrintWindow, instance).__init__()
                cls._instance = instance
            except Exception as e:
                _safe_stderr(f"窗口创建错误: {str(e)}")
                traceback.print_exc(file=sys.__stderr__)
            finally:
                cls._lock = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            try:
                self.initialized = True
                self.setup_ui()
            except Exception as e:
                _safe_stderr(f"窗口初始化错误: {str(e)}")
                traceback.print_exc(file=sys.__stderr__)

    def setup_ui(self):
        self.setWindowTitle("控制台输出")
        self.resize(1000, 800)
        # 隐藏关闭按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 20px;
                padding: 15px;
                line-height: 150%;
            }
        """)
        self.text_area.document().setMaximumBlockCount(1000)
        layout.addWidget(self.text_area)
        self.setLayout(layout)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.width() - 50, 50)

    def append_text(self, text):
        try:
            if not text:
                return
            self.text_area.append(str(text))
            QApplication.processEvents()
            scrollbar = self.text_area.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except Exception as e:
            _safe_stderr(f"文本追加错误: {str(e)}")
            traceback.print_exc(file=sys.__stderr__)

    def closeEvent(self, event):
        # 禁止关闭窗口
        event.ignore()

class PrintDispatcher(QObject):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.log_signal.connect(self._main_thread_print)

    def _main_thread_print(self, msg):
        # 只在主线程调用uiprint.print
        _uiprint_print(msg)

_dispatcher = PrintDispatcher()

def safe_print(*args, sep=' ', end='\n'):
    msg = sep.join(str(arg) for arg in args) + end
    if threading.current_thread() == threading.main_thread():
        _uiprint_print(msg.rstrip())
    else:
        _dispatcher.log_signal.emit(msg.rstrip())

def _uiprint_print(*args, sep=' ', end='\n'):
    # 原有uiprint.print逻辑
    try:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        window = PrintWindow()
        if not window.isVisible():
            window.show()
        text = sep.join(str(arg) for arg in args) + end
        window.append_text(text.rstrip())
    except Exception as e:
        _safe_stderr(f"打印错误: {str(e)}")
        traceback.print_exc(file=sys.__stderr__)

# 保持原有print接口兼容
def print(*args, sep=' ', end='\n'):
    safe_print(*args, sep=sep, end=end)