from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox, QHeaderView
)
from PyQt5.QtCore import Qt
import os
import subprocess
import sys
from src.ui.uiprint import print

class ShowTargetFiles(QWidget):
    def __init__(self, files=None):
        super().__init__()
        self.files = files or []
        self.setWindowTitle("搜索结果")
        self.resize(2200, 800)  # 窗口大小翻倍
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["文件路径", "文件名", "类型", "大小(字节)", "描述"]
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellDoubleClicked.connect(self.open_file)

        # 设置表头和列宽
        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.Interactive)  # 每一列都可拖动
        header.setStretchLastSection(False)
        # 设置初始列宽
        self.table.setColumnWidth(0, 640)
        self.table.setColumnWidth(1, 360)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 700)

        # 允许水平滚动
        self.table.setHorizontalScrollMode(QTableWidget.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableWidget.ScrollPerPixel)

        # 浅色整体风格
        self.table.setStyleSheet("""
            QTableWidget {
                background: #fafbfc;
                color: #222;
                gridline-color: #e0e0e0;
                font-size: 16px;
                selection-background-color: #cce6ff;
                selection-color: #222;
            }
            QHeaderView::section {
                background-color: #f5f6fa;
                color: #222;
                font-weight: bold;
                font-size: 16px;
                padding: 8px;
                border-right: 2px solid #e0e0e0;
                border-bottom: 2px solid #e0e0e0;
            }
            QTableWidget::item {
                border-right: 1px solid #e0e0e0;
                background: #ffffff;
                color: #222;
            }
            QTableWidget::item:selected {
                background: #cce6ff;
                color: #222;
            }
        """)

        layout.addWidget(self.table)

        btn_close = QPushButton("关闭")
        btn_close.setFixedHeight(32)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #f5f6fa;
                color: #222;
                font-size: 16px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 6px 18px;
            }
            QPushButton:hover {
                background: #e6f2ff;
            }
        """)
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
            def create_item(text, tooltip=True):
                item = QTableWidgetItem(str(text))
                if tooltip:
                    item.setToolTip(str(text))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                return item

            path = str(file_info.get("file_path", ""))
            self.table.setItem(row, 0, create_item(path))
            self.table.setItem(row, 1, create_item(file_info.get("file_name", "")))
            self.table.setItem(row, 2, create_item(file_info.get("file_type", "")))
            self.table.setItem(row, 3, create_item(file_info.get("file_size", ""), False))
            self.table.setItem(row, 4, create_item(file_info.get("short_description", "")))

        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 40)

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