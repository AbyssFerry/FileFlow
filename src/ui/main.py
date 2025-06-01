#仅供测试用！！！！！！！！！

import sys
from PyQt5.QtWidgets import QApplication
from get_user_choice import UserChoiceWidget
from drop_dispatcher import DropDispatcherWidget
from get_user_search import UserSearchWidget
from show_progress_bar import ProgressBarWidget
from PyQt5.QtCore import QTimer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_choice_widget = UserChoiceWidget()
    drop_dispatcher_widget = DropDispatcherWidget()
    user_search_widget = UserSearchWidget()
    progress_widget = ProgressBarWidget()

    def on_choice_made(choice):
        if choice == "drop":
            drop_dispatcher_widget.show()
        elif choice == "search":
            user_search_widget.show()

    def start_progress_simulation():
        progress_value = 0
        progress_widget.start_progress()  # 已包含 show()

        def update():
            nonlocal progress_value
            progress_value += 5
            progress_widget.update_progress(progress_value)
            if progress_value >= 100:
                timer.stop()
                progress_widget.confirm_button.setVisible(True)  # 直接显示确认按钮

        timer = QTimer()
        timer.timeout.connect(update)
        timer.start(50)

    drop_dispatcher_widget.file_dropped.connect(
        lambda path: (print(f"拖入路径：{path}"), start_progress_simulation())
    )
    drop_dispatcher_widget.folder_dropped.connect(
        lambda path: (print(f"拖入路径：{path}"), start_progress_simulation())
    )

    user_search_widget.search_submitted.connect(lambda text: print(f"用户查询内容为：{text}"))

    user_choice_widget.choice_made.connect(on_choice_made)

    user_choice_widget.show()

    sys.exit(app.exec_())





