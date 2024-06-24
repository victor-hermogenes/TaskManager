from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QComboBox
from PyQt5.QtCore import QSize
from database.db_handler import DBHandler
from models.task import Task


class TaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.db_handler = DBHandler()   # Initialize the database handler

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

        self.load_tasks()
    

    def load_tasks(self):
        tasks = self.db_handler.get_tasks()
        for task in tasks:
            self.add_task_to_list(task.name, task.status, add_to_db=False)

    
    def add_task(self):
        task_name = self.task_input.text()
        if task_name:
            self.add_task_to_list(task_name)
            self.task_input.clear()

    
    def add_task_to_list(self, task_name, status="To do", add_to_db=True):
        task_item_widget = TaskItem(task_name, self.remove_task, status)
        task_item = QListWidgetItem(self.task_list)
        task_item.setSizeHint(task_item_widget.sizeHint())
        self.task_list.addItem(task_item)
        self.task_list.setItemWidget(task_item, task_item_widget)
        if add_to_db:
            new_task = Task(name=task_name, status=task_item_widget.status_dropdown.currentText())
            self.db_handler.add_task(new_task)
        return task_item_widget

    
    def remove_task(self, task_item_widget):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget is task_item_widget:
                self.task_list.takeItem(i)
                break


class TaskItem(QWidget):
    def __init__(self, task_name, delete_callback, status="To do"):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.label = QLabel(task_name, self)

        # Status Dropdown
        self.status_dropdown = QComboBox(self)
        self.status_dropdown.addItems(["To do", "On Going", "Done", "Late", "Cancelled"])
        self.status_dropdown.setCurrentText(status)

        # Red "X" button for deletion
        self.delete_button = QPushButton("X", self)
        self.delete_button.setStyleSheet("QPushButton {color: red; font-weight: bold; }")
        self.delete_button.setFixedSize(QSize(30, 30))
        self.delete_button.clicked.connect(self.delete_task)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.status_dropdown)
        self.layout.addWidget(self.delete_button)

        self.delete_callback = delete_callback

    
    def delete_task(self):
        self.delete_callback(self)
