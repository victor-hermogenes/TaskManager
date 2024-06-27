from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QComboBox, QCheckBox, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, Qt
from database.models import create_task, get_all_users
from utils.validators import validate_task
from utils.helpers import checkboxes_to_list


class CreateTaskWindow(QWidget):
    task_created = pyqtSignal()  # Signal to indicate task creation

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Create Task")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()

    
    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Title")
        self.title_input = QLineEdit()
        self.description_label = QLabel("Description")
        self.description_input = QTextEdit()
        self.start_date_label = QLabel("Start Date")
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.due_date_label = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        self.priority_label = QLabel("Priority")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.checkboxes_label = QLabel("Subtasks")
        self.checkboxes_layout = QVBoxLayout()

        self.add_checkbox_button = QPushButton("Add Subtask")
        self.add_checkbox_button.clicked.connect(self.add_checkbox)

        self.assigned_users_label = QLabel("Assign to Users")
        self.assigned_users_list = QListWidget()
        self.assigned_users_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_users()

        self.create_button = QPushButton("Create Task")
        self.create_button.clicked.connect(self.create_task)

        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.due_date_label)
        layout.addWidget(self.due_date_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.checkboxes_label)
        layout.addLayout(self.checkboxes_layout)
        layout.addWidget(self.add_checkbox_button)
        layout.addWidget(self.assigned_users_label)
        layout.addWidget(self.assigned_users_list)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    
    def load_users(self):
        users = get_all_users()
        for user_id, username in users:
            item = QListWidgetItem(username)
            item.setData(Qt.UserRole, user_id)
            self.assigned_users_list.addItem(item)


    def add_checkbox(self):
        checkbox = QCheckBox("New Subtask")
        self.checkboxes_layout.addWidget(checkbox)

        
    def create_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()
        checkboxes = checkboxes_to_list(self.checkboxes_layout)
        assignees = [item.data(Qt.UserRole) for item in self.assigned_users_list.selectedItems()]
        priority = self.priority_input.currentText()

        is_valid, message = validate_task(title, start_date, due_date)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        create_task(self.user_id, title, description, start_date, due_date, status, checkboxes, assignees, priority)
        self.task_created.emit()
        QMessageBox.information(self, "Success", "Task created successfully")
        self.close()