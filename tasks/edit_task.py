from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QComboBox, QCheckBox, QHBoxLayout, QMessageBox
from database.models import update_task
from utils.validators import validate_task  # Import task validator
from utils.helpers import checkboxes_to_list, format_date  # Import helpers


class EditTaskWindow(QWidget):
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
        self.description_input = QLineEdit(self.task[3])
        self.start_date_label = QLabel("Start Date")
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(self.task[4])
        self.due_date_label = QLabel("Due date")
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(self.task[5])
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.status_input.addItems(["Not Started", "In Progress", "Completed"])
        self.status_input.setCurrentText(self.task[6])
        self.checkboxes_label = QLabel("Subtasks")
        self.checkboxes_layout = QVBoxLayout()
        checkboxes = self.task[7].split(',')

        for checkbox_text in checkboxes:
            checkbox = QCheckBox(checkbox_text)
            self.checkboxes_layout.addWidget(checkbox)

        self.add_checkbox_button = QPushButton("Add Subtask")
        self.add_checkbox_button.clicked.connect(self.add_checkbox)

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
        layout.addWidget(self.checkboxes_layout)
        layout.addWidget(self.add_checkbox_button)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    
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

        is_valid, message = validate_task(title, start_date, due_date)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        update_task(self.task[0], title, description, start_date, due_date, status, checkboxes)
        QMessageBox.information(self, "Success", "Task updated successfully")
        self.close()