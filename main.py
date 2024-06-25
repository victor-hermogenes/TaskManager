from PyQt5.QtWidgets import QApplication
import sys
from auth.login import LoginWindow


def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()