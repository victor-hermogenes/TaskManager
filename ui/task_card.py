from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import pyqtSignal

class TaskCard(QWidget):
    edit_requested = pyqtSignal(tuple)


    def __init__(self, task):
        super().__init__()
        self.task = task
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        self.title_label = QLabel(self.task[2])
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.title_label)

        self.description_label = QLabel(self.task[3])
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        date_layout = QHBoxLayout()
        self.start_date_label = QLabel(f"Start: {self.task[4]}")
        self.due_date_label = QLabel(f"Due: {self.task[5]}")
        date_layout.addWidget(self.start_date_label)
        date_layout.addWidget(self.due_date_label)
        layout.addLayout(date_layout)

        self.status_label = QLabel(f"Status: {self.task[6]}")
        layout.addWidget(self.status_label)

        self.priority_label = QLabel(f"Priority: {self.task[8]}")
        layout.addWidget(self.priority_label)

        # Assignees
        self.assignees_label = QLabel(f"Assignees: {self.task[9]}")  # Assignees are at index 8
        layout.addWidget(self.assignees_label)

        self.checkbox_layout = QVBoxLayout()
        checkboxes = self.task[7].split(',')
        for checkbox_text in checkboxes:
            checkbox = QCheckBox(checkbox_text)
            checkbox.setChecked(True)
            checkbox.setDisabled(True)
            self.checkbox_layout.addWidget(checkbox)
        layout.addLayout(self.checkbox_layout)

        self.edit_button = QPushButton("Edit")
        self.edit_button.clicked.connect(self.request_edit)
        layout.addWidget(self.edit_button)

        self.setLayout(layout)


    def request_edit(self):
        self.edit_requested.emit(self.task)


    def view_details(self):
        from tasks.task_view import TaskViewWindow
        self.view_window = TaskViewWindow(self.task)
        self.view_window.show()