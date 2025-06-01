#拖入文件目录

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class InitFolderWidget(QWidget):
    folder_dropped = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("拖入目录")
        self.resize(400, 300)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        self.label = QLabel("请拖入文件夹")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                import os
                if os.path.isdir(path):
                    event.acceptProposedAction()

    def dropEvent(self, event):
        url = event.mimeData().urls()[0]
        path = url.toLocalFile()
        self.folder_dropped.emit(path)

