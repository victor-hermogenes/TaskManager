from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout
from database.models import get_tasks_by_user


class TaskViewWindow(QWidget):
    def __init__(self, task):
        super().__init__()
        self.task = task
        self.setWindowTitle("View Task")
        self.setGeometry(100, 100, 400, 400)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()
        self.title_label = QLabel(f"Title: {self.task[2]}")
        self.description_label = QLabel(f"Description: {self.task[3]}")
        self.start_date_label = QLabel(f"Start Date: {self.task[4]}")
        self.due_date_label = QLabel(f"Due Date: {self.task[5]}")
        self.status_label = QLabel(f"Status: {self.task[6]}")
        self.checkboxes_label = QLabel("Subtasks:")

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.due_date_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.checkboxes_label)

        self.checkboxes_layout = QVBoxLayout()
        checkboxes = self.task[7].split(',')
        for checkbox_text in checkboxes:
            checkbox = QCheckBox(checkbox_text)
            checkbox.setChecked(True)
            checkbox.setDisabled(True)
            self.checkboxes_layout.addWidget(checkbox)

        layout.addLayout(self.checkboxes_layout)
        self.edit_button = QPushButton("Edit Task")
        self.edit_button.clicked.connect(self.edit_task)
        layout.addWidget(self.edit_button)

        self.setLayout(layout)


    def edit_task(self):
        from tasks.edit_task import EditTaskWindow
        self.edit_window = EditTaskWindow(self.task)
        self.edit_window.show()
        self.close()

    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # Sample task data for testing
    task = (1, 1, "Sample Task", "This is a description of the sample task.", "2024-06-24", "2024-07-01", "In Progress", "Subtask 1,Subtask 2, Substask 3")

    view_window = TaskViewWindow(task)
    view_window.show()

    sys.exit(app.exec_)