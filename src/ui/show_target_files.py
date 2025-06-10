from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys

class ShowTargetFiles(QWidget):
    def __init__(self, files=None):
        super().__init__()
        self.files = files or []
        self.setWindowTitle("搜索结果")
        self.resize(800, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["文件路径", "文件名", "类型", "大小(字节)", "描述"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellDoubleClicked.connect(self.open_file)

        # 表头样式
        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
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
        if not self.files:
            self.table.setRowCount(0)
            return
            
        self.table.setRowCount(len(self.files))
        for row, file_info in enumerate(self.files):
            self.table.setItem(row, 0, QTableWidgetItem(str(file_info.get("file_path", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(file_info.get("file_name", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(file_info.get("file_type", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(file_info.get("file_size", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(str(file_info.get("short_description", ""))))

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