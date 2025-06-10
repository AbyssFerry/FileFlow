# show_target_files.py

from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys

class ShowTargetFiles(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("目标文件列表")
        self.resize(800, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["文件路径", "文件名字", "类型", "大小(字节)", "描述"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellDoubleClicked.connect(self.open_file)

        # 表头样式
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 第一列拉伸
        for i in range(1, 5):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        self.table.setStyleSheet("""
            QTableWidget::item { padding: 6px; }
            QHeaderView::section {
                background-color: #f0f0f0;
                font-weight: bold;
                padding: 4px;
            }
        """)

        layout.addWidget(self.table)

        # 关闭按钮
        btn_close = QPushButton("关闭")
        btn_close.setFixedHeight(32)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        # 模拟数据
        files = [
            {
                "file_path": "/path/to/file1.txt",
                "file_name": "file1.txt",
                "file_type": "txt",
                "file_size": 1024,
                "short_description": "这是一个文本文件"
            },
            {
                "file_path": "/path/to/file2.jpg",
                "file_name": "file2.jpg",
                "file_type": "jpg",
                "file_size": 2048,
                "short_description": "这是一个图片文件"
            },
            {
                "file_path": "/path/to/file3.pdf",
                "file_name": "file3.pdf",
                "file_type": "pdf",
                "file_size": 3072,
                "short_description": "这是一个PDF文档"
            }
        ]

        self.table.setRowCount(len(files))
        for row, f in enumerate(files):
            self.table.setItem(row, 0, QTableWidgetItem(f["file_path"]))
            self.table.setItem(row, 1, QTableWidgetItem(f["file_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(f["file_type"]))
            self.table.setItem(row, 3, QTableWidgetItem(str(f["file_size"])))
            self.table.setItem(row, 4, QTableWidgetItem(f["short_description"]))

    def open_file(self, row, _column):
        file_path = self.table.item(row, 0).text()
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "文件不存在", f"文件路径不存在:\n{file_path}")
            return
        try:
            if sys.platform.startswith('darwin'):
                subprocess.call(('open', file_path))
            elif os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            QMessageBox.warning(self, "打开失败", f"无法打开文件:\n{file_path}\n错误: {e}")
