import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from auth.auth import login_user


class LoginWindow(QDialog):
    show_register_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.username = ""
        self.role = ""
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

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

        success, role = login_user(username, password)
        if success:
            QMessageBox.information(self, "Success", "Login successful")
            self.username = username
            self.role = role
            self.accept()  # Fecha o diálogo de login e continua para a janela principal
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")


    def show_register(self):
        self.show_register_window.emit()
        self.hide()  # Esconde a janela de login mas não a fecha

    def get_user_info(self):
        return self.username, self.role


    def open_main_window(self, username):
        from ui.main_window import MainWindow
        self.main_window = MainWindow(username)
        self.main_window.show()
        self.close()