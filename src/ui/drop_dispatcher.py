#该模块用来判断拖入的是文件目录还是文件

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
import os

class DropDispatcherWidget(QWidget):
    folder_dropped = pyqtSignal(str)
    file_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("请拖入文件目录或者文件")
        self.resize(400, 200)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        self.info_label = QLabel("请拖入文件目录或者文件")
        self.drop_area = QTextEdit()
        self.drop_area.setReadOnly(True)

        layout.addWidget(self.info_label)
        layout.addWidget(self.drop_area)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            path = url.toLocalFile()
            self.drop_area.setText(path)
            if os.path.isdir(path):
                self.folder_dropped.emit(path)
            elif os.path.isfile(path):
                self.file_dropped.emit(path)
            return