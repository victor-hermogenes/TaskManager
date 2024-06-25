# task_manager/ui/task_card.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt

class TaskCard(QWidget):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel(self.task[2])
        self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(self.title_label)

        # Description
        self.description_label = QLabel(self.task[3])
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        # Dates
        date_layout = QHBoxLayout()
        self.start_date_label = QLabel(f"Start: {self.task[4]}")
        self.due_date_label = QLabel(f"Due: {self.task[5]}")
        date_layout.addWidget(self.start_date_label)
        date_layout.addWidget(self.due_date_label)
        layout.addLayout(date_layout)

        # Status
        self.status_label = QLabel(f"Status: {self.task[6]}")
        layout.addWidget(self.status_label)

        # Checkboxes
        self.checkbox_layout = QVBoxLayout()
        checkboxes = self.task[7].split(',')
        for checkbox_text in checkboxes:
            checkbox = QCheckBox(checkbox_text)
            checkbox.setChecked(True)
            checkbox.setDisabled(True)
            self.checkbox_layout.addWidget(checkbox)
        layout.addLayout(self.checkbox_layout)

        # View Details Button
        self.view_button = QPushButton("View Details")
        self.view_button.clicked.connect(self.view_details)
        layout.addWidget(self.view_button)

        self.setLayout(layout)

    def view_details(self):
        from tasks.task_view import TaskViewWindow
        self.view_window = TaskViewWindow(self.task)
        self.view_window.show()