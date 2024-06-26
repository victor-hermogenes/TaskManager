from PyQt5.QtWidgets import QApplication, QDialog
import sys
from auth.login import LoginWindow
from ui.main_window import MainWindow
from auth.register import RegisterWindow

def main():
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    register_window = RegisterWindow()

    login_window.show_register_window.connect(register_window.show)
    register_window.show_login_window.connect(login_window.show)

    if login_window.exec_() == QDialog.Accepted:
        username, role = login_window.get_user_info()
        main_window = MainWindow(username)
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()