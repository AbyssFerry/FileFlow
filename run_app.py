import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.ui.get_user_choice import GetUserChoice

# 设置高分屏支持
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

def main():
    try:
        # 禁用高DPI缩放
        QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        app = QApplication(sys.argv)
        
        # 设置默认字体
        default_font = QFont("Microsoft YaHei UI", 9)
        app.setFont(default_font)
        
        window = GetUserChoice()
        # window.show()  # 删除这行，让窗口自己控制显示
        
        return app.exec_()
    except Exception as e:
        print(f"程序发生错误: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
