from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from auth.auth import register_user
from utils.validators import validate_username, validate_password   # Import validators


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    
    def initUI(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.confirm_label = QLabel("Confirm Password")
        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Register")
        self.back_button = QPushButton("Back to Login")

        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(self.show_login)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_input.text()

        is_valid, message = validate_username(username)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return
        
        is_valid, message = validate_password(password)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        if register_user(username, password):
            QMessageBox.information(self, "Success", "Registration successful")
            self.show_login()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")
        

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
    
from auth.login import LoginWindow