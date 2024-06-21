from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem


class TaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Enter a new task")

        self.add_task_button = QPushButton("Add Task", self)
        self.add_task_button.clicked.connect(self.add_task)

        self.task_list = QListWidget(self)
        self.task_list.setDragDropMode(QListWidget.InternalMove)

        self.layout.addWidget(self.task_input)
        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.task_list)

    
    def add_task(self):
        task_name = self.task_input.text()
        if task_name:
            task_item = QListWidgetItem(task_name)
            self.task_list.addItem(task_item)
            self.task_input.clear()