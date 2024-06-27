from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, QMenuBar, QAction, QProgressBar
from auth.auth import register_user
from utils.validators import validate_username, validate_password    # Import validators
from utils.password_strengh import evaluate_password_strength    # Import password strength evaluator    
from ui.dark_mode import apply_dark_mode
from ui.light_mode import apply_light_mode

CONFIG_FILE = 'config.txt'


def save_style_preference(style):
    with open(CONFIG_FILE, 'w') as f:
        f.write(style)


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
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
        self.username_input.textChanged.connect(self.check_username_availability)   # Connect text change username availability
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.textChanged.connect(self.update_password_strength)  # Connect text change to update password strength
        self.password_strength_bar = QProgressBar()
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
        layout.addWidget(self.password_strength_bar)
        layout.addWidget(self.confirm_label)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    
    def check_username_availability(self):
        username = self.username_input.text()

        from auth.auth import is_username_available

        if not is_username_available(username):
            self.username_input.setStyleSheet("border: 1px solid red;")
        else:
            self.username_input.setStyleSheet("border: 1px solid green;")


    def update_password_strength(self):
        password = self.password_input.text()
        strength = evaluate_password_strength(password)
        self.password_strength_bar.setValue(strength * 20)    # Set progress bar value based on strength

    
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

    def set_light_mode(self):
        apply_light_mode(QApplication.instance())
        save_style_preference('light')
    

    def set_dark_mode(self):
        apply_dark_mode(QApplication.instance())
        save_style_preference('dark')
    
from auth.login import LoginWindow