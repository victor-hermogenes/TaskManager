from PyQt5.QtWidgets import QApplication
import sys
from auth.login import LoginWindow
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    login_window.login_successful.connect(show_main_window)
    login_window.show()

    sys.exit(app.exec_())


def show_main_window(username):
    main_window = MainWindow(username)
    main_window.show()

if __name__ == "__main__":
    main()