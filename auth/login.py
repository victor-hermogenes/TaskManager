from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from auth.auth import login_user


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
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

        if login_user(username, password):
            QMessageBox.information(self, "Success", "Login successful")
            self.close()  # Proceed to the main window
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

        
    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

from auth.register import RegisterWindow