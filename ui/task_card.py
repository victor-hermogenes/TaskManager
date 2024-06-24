from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt


class TaskCard(QWidget):
    def __init__(self, task_id, title, description, start_date, due_date, status, checkboxes):
        super().__init__()
        self.task_id = task_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.status = status
        self.checkboxes = checkboxes

        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        # Title
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-weight; font-size> 16px;")
        layout.addWidget(self.title_label)

        # Description
        self.description_label = QLabel(self.description)
        self.description_label.setWordWrap(True)
        layout.addWidget(self.description_label)

        # Dates
        date_layout = QHBoxLayout()
        self.start_date_label = QLabel(f"Start: {self.start_date}")
        self.due_date_label = QLabel(f"Due: {self.due_date}")
        date_layout.addWidget(self.start_date_label)
        date_layout.addWidget(self.due_date_label)
        layout.addLayout(date_layout)

        # Status
        self.status_label = QLabel(f"Status: {self.status}")
        layout.addWidget(self.status_label)

        # Checkboxes
        self.checkboxes_layout = QVBoxLayout()
        for checkbox_text in self.checkboxes:
            checkbox = QCheckBox(checkbox_text)
            self.checkbox_layout.addWidget(checkbox)
        layout.addLayout(self.checkbox_layout)

        # View Details Button
        self.view_button = QPushButton("View Details")
        self.view_button.clicked.connect(self.view_details)
        layout.addWidget(self.view_button)

        self.setLayout(layout)

    
    def view_details(self):
        # Placeholder for viewing detailed task info
        print(f"Viewing details for task: {self.task_id}")

    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)

    # Sample data for testing
    task_id = 1
    title = "Sample Task"
    description = "This is a description of the sample task"
    start_date = "2024-06-24"
    due_date = "2024-07-01"
    status = "In Progress"
    checkboxes = ["Subtask 1", "Subtask 2", "Subtask 3"]

    task_card = TaskCard(task_id, title, description, start_date, due_date, status, checkboxes)
    task_card.show()

    sys.exit(app.exec_())