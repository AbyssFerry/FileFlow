#仅供测试用！！！！！！！！！！！

import sys
from PyQt5.QtWidgets import QApplication
from get_user_choice import GetUserChoice


def main():
    app = QApplication(sys.argv)
    window = GetUserChoice()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()







