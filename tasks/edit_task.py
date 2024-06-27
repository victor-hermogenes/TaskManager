from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QComboBox, QCheckBox, QMessageBox, QListWidget, QListWidgetItem
from PyQt5.QtCore import QDate, pyqtSignal, Qt
from database.models import update_task, get_all_users, get_assignees_by_task
from utils.validators import validate_task
from utils.helpers import checkboxes_to_list


class EditTaskWindow(QWidget):
    task_updated = pyqtSignal()  # Signal to indicate task update

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setWindowTitle("Edit Task")
        self.setGeometry(100, 100, 400, 600)
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
        self.priority_label = QLabel("Priority")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High"])
        self.priority_input.setCurrentText(self.task[8])
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

        self.assigned_users_label = QLabel("Assign to Users")
        self.assigned_users_list = QListWidget()
        self.assigned_users_list.setSelectionMode(QListWidget.MultiSelection)
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
        layout.addWidget(self.priority_label)
        layout.addWidget(self.priority_input)
        layout.addWidget(self.checkboxes_label)
        layout.addLayout(self.checkboxes_layout)
        layout.addWidget(self.add_checkbox_button)
        layout.addWidget(self.assigned_users_label)
        layout.addWidget(self.assigned_users_list)
        layout.addWidget(self.update_button)

        self.setLayout(layout)


    def load_users(self):
        users = get_all_users()
        for user_id, username in users:
            item = QListWidgetItem(username)
            item.setData(Qt.UserRole, user_id)
            self.assigned_users_list.addItem(item)

        current_assignees = get_assignees_by_task(self.task[0])
        for user_id, username in current_assignees:
            items = self.assigned_users_list.findItems(username, Qt.MatchExactly)
            if items:
                item = items[0]
                item.setSelected(True)


    
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
        assignees = [item.data(Qt.UserRole) for item in self.assigned_users_list.selectedItems()]
        priority = self.priority_input.currentText()

        is_valid, message = validate_task(title, start_date, due_date)
        if not is_valid:
            QMessageBox.warning(self, "Error", message)
            return

        update_task(self.task[0], title, description, start_date, due_date, status, checkboxes, assignees, priority)  # Pass all arguments
        self.task_updated.emit()
        QMessageBox.information(self, "Success", "Task updated successfully")
        self.close()