from PyQt5.QtWidgets import QApplication
import sys
from auth.login import LoginWindow
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    login_window = LoginWindow()


    def on_login_success(username):
        login_window.close()
        main_window = MainWindow(username)
        main_window.show()

    login_window.login_successful.connect(on_login_success)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()