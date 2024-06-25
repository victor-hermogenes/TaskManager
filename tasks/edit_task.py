from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QComboBox, QCheckBox, QMessageBox
from PyQt5.QtCore import QDate, pyqtSignal
from database.models import update_task, get_all_users
from utils.validators import validate_task
from utils.helpers import checkboxes_to_list


class EditTaskWindow(QWidget):
    task_updated = pyqtSignal()  # Signal to indicate task update

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setWindowTitle("Edit Task")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Title")
        self.title_input = QLineEdit(self.task[2])
        self.description_label = QLabel("Description")
        self.description_input = QTextEdit(self.task[3])
        self.start_date_label = QLabel("Start Date")
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.fromString(self.task[4], "yyyy-MM-dd"))
        self.due_date_label = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.fromString(self.task[5], "yyyy-MM-dd"))
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        self.status_input.setCurrentText(self.task[6])
        self.checkboxes_label = QLabel("Subtasks")
        self.checkboxes_layout = QVBoxLayout()
        checkboxes = self.task[7].split(',')

        for checkbox_text in checkboxes:
            checkbox = QCheckBox(checkbox_text)
            checkbox.setChecked(True)
            self.checkboxes_layout.addWidget(checkbox)

        self.add_checkbox_button = QPushButton("Add Subtask")
        self.add_checkbox_button.clicked.connect(self.add_checkbox)

        self.assigned_user_label = QLabel("Assign to User")
        self.assigned_user_input = QComboBox()
        self.load_users()

        self.update_button = QPushButton("Update Task")
        self.update_button.clicked.connect(self.update_task)

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
        layout.addWidget(self.checkboxes_label)
        layout.addLayout(self.checkboxes_layout)
        layout.addWidget(self.add_checkbox_button)
        layout.addWidget(self.assigned_user_label)
        layout.addWidget(self.assigned_user_input)
        layout.addWidget(self.update_button)

        self.setLayout(layout)


    def load_users(self):
        users = get_all_users()
        for user_id, username in users:
            self.assigned_user_input.addItem(username, user_id)
        # Set the current assigned user
        assigned_user_id = self.task[1]
        index = self.assigned_user_input.findData(assigned_user_id)
        if index >= 0:
            self.assigned_user_input.setCurrentIndex(index)

    
    def add_checkbox(self):
        checkbox = QCheckBox("New Subtask")
        self.checkboxes_layout.addWidget(checkbox)

    
    def update_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()
        checkboxes = checkboxes_to_list(self.checkboxes_layout)
        assigned_user_id = self.assigned_user_input.currentData()

        is_valid, message = validate_task(title, start_date, due_date)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        update_task(self.task[0], assigned_user_id, title, description, start_date, due_date, status, checkboxes)
        self.task_updated.emit()
        QMessageBox.information(self, "Success", "Task updated successfully")
        self.close()