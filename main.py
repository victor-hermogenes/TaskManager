from PyQt5.QtWidgets import QApplication, QDialog
import sys
from auth.login import LoginWindow
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    
    if login_window.exec_() == QDialog.Accepted:
        username, role = login_window.get_user_info()
        main_window = MainWindow(username, role)
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()