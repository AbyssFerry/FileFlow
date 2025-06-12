import sys
import os
from multiprocessing import freeze_support
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.ui.get_user_choice import GetUserChoice

# 添加freeze_support，支持打包多进程
if __name__ == "__main__":
    freeze_support()
    
    # 设置环境变量，防止子进程重新加载主程序
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["PYTHONOPTIMIZE"] = "1"  # 防止子进程重新加载主程序
    
    # 禁用高DPI缩放（保持原始代码的设置）
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    
    # 设置默认字体
    default_font = QFont("Microsoft YaHei UI", 9)
    app.setFont(default_font)
    
    window = GetUserChoice()
    # window.show()  # 由窗口自己控制显示
    
    sys.exit(app.exec_())
