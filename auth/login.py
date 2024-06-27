import sys
import os

# Ensure the directory containing the 'task_card' module is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMenuBar, QAction, QApplication
from PyQt5.QtCore import pyqtSignal
from auth.auth import login_user
from ui.dark_mode import apply_dark_mode
from ui.light_mode import apply_light_mode


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


    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if login_user(username, password):
            QMessageBox.information(self, "Success", "Login successful")
            self.login_successful.emit(username)  # Emit the signal with the username
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")


    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    def set_light_mode(self):
        apply_light_mode(QApplication.instance())


    def set_dark_mode(self):
        apply_dark_mode(QApplication.instance())

from auth.register import RegisterWindow