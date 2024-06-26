import sys
import os

# Ensure the directory containing the 'task_card' module is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMenuBar, QAction, QApplication, QProgressDialog
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from auth.auth import login_user
from ui.dark_mode import apply_dark_mode
from ui.light_mode import apply_light_mode
from worker import Worker

CONFIG_FILE = 'config.txt'


def save_style_preference(style):
    with open(CONFIG_FILE, 'w') as f:
        f.write(style)


class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)  # Signal to indicate successful login with username


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        menu_bar = QMenuBar(self)

        view_menu = menu_bar.addMenu("View")
        
        light_mode_action = QAction("Light Mode", self)
        dark_mode_action = QAction("Dark Mode", self)

        light_mode_action.triggered.connect(self.set_light_mode)
        dark_mode_action.triggered.connect(self.set_dark_mode)

        view_menu.addAction(light_mode_action)
        view_menu.addAction(dark_mode_action)

        layout.setMenuBar(menu_bar)

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.show_register)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    
    def show_loading_dialog(self, message="Loading..."):
        self.loading_dialog = QProgressDialog(message, None, 0, 0, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.setCancelButton(None)
        self.loading_dialog.show()


    def hide_loading_dialog(self):
        self.loading_dialog.hide()


    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        self.show_loading_dialog("Logging in...")


        def login_func(username, password):
            return login_user(username, password)

        self.thread = QThread()
        self.worker = Worker(login_func, username, password)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.result.connect(self.handle_login_result)
        self.thread.start()


    def handle_login_result(self, success):
        self.hide_loading_dialog()
        if success:
            QMessageBox.information(self, "Success", "Login successful")
            self.login_successful.emit(self.username_input.text())  # Emit the signal with the username
            self.open_main_window(self.username_input.text())  # Proceed to the main window
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")
    

    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    def set_light_mode(self):
        apply_light_mode(QApplication.instance())
        save_style_preference('light')


    def set_dark_mode(self):
        apply_dark_mode(QApplication.instance())
        save_style_preference('dark')

    
    def open_main_window(self, username):
        from ui.main_window import MainWindow
        self.main_window = MainWindow(username)
        self.main_window.show()
        self.close()

from auth.register import RegisterWindow