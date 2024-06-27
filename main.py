from PyQt5.QtWidgets import QApplication
import sys
import os
from auth.login import LoginWindow
from ui.main_window import MainWindow
from ui.dark_mode import apply_dark_mode
from ui.light_mode import apply_light_mode

CONFIG_FILE = 'config.txt'


def load_style_preference():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().strip()
    return 'light'


def save_style_preference(style):
    with open(CONFIG_FILE, 'w') as f:
        f.write(style)


def apply_saved_style(app):
    style = load_style_preference()
    if style == 'dark':
        apply_dark_mode(app)
    else:
        apply_light_mode(app)


def main():
    app = QApplication(sys.argv)

    apply_saved_style(app)

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