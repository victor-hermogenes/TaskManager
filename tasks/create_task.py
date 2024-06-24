from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QDateEdit, QPushButton, QComboBox, QCheckBox, QHBoxLayout, QMessageBox
from database.models import create_task


class CreateTaskWindow(QWidget):
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
        self.description_input = QLineEdit()
        self.start_date_label = QLabel("Start Date")
        self.start_date_input = QDateEdit()
        self.due_date_label = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.status_label = QLabel("Status")
        self.status_input = QComboBox()
        self.Status_input.additems(["Not Started", "In Progress", "Completed"])
        self.checkboxes_label = QLabel("Subtasks")
        self.checkboxes_layout = QVBoxLayout

        self.add_checkbox_buttton = QPushButton("Add Substask")
        self.add_checkbox_buttton.clicked.connect(self.add_checkbox)

        self.create_button = QPushButton("Create Tasks")
        self.add_checkbox_buttton.clicked.connect(self.create_task)

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
        layout.addWidget(self.add_checkbox_buttton)
        layout.addWidget(self.create_button)

        self.setLayout

    def add_checkbox(self):
        checkbox = QCheckBox("New Subtask")
        self.checboxes_layout.addWidget(checkbox)

        
    def create_task(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()
        checkboxes = [self.checkboxes_layout.itemAt(i).widget().text() for i in range(self.checkboxes_layout.count())]

        create_task(self.user_id, title, description, start_date, due_date, status, checkboxes)
        QMessageBox.information(self, "Success", "Task created successfully")
        self.close()