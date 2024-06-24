from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QComboBox
from PyQt5.QtCore import QSize
from database.db_handler import DBHandler
from models.task import Task
from ui.task_edit_window import TaskEditWindow

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
            self.add_task_to_list(task.name, task.status, task.description, task.start_date, task.due_date, task.checkboxes, add_to_db=False)

    def add_task(self):
        task_name = self.task_input.text()
        if task_name:
            self.add_task_to_list(task_name)
            self.task_input.clear()

    def add_task_to_list(self, task_name, status="To do", description="", start_date="", due_date="", checkboxes=None, add_to_db=True):
        if checkboxes is None:
            checkboxes = []
        task_item_widget = TaskItem(task_name, self.update_task, self.remove_task, status, self.open_edit_window, description, start_date, due_date, checkboxes)
        task_item = QListWidgetItem(self.task_list)
        task_item.setSizeHint(task_item_widget.sizeHint())
        self.task_list.addItem(task_item)
        self.task_list.setItemWidget(task_item, task_item_widget)
        if add_to_db:
            new_task = Task(name=task_name, status=task_item_widget.status_dropdown.currentText(), description=description, start_date=start_date, due_date=due_date, checkboxes=checkboxes)
            self.db_handler.add_task(new_task)
        return task_item_widget

    def update_task(self, task_item_widget):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget is task_item_widget:
                task_name = widget.label.text()
                task_status = widget.status_dropdown.currentText()
                task_description = widget.description
                task_start_date = widget.start_date
                task_due_date = widget.due_date
                task_checkboxes = widget.checkboxes
                updated_task = Task(name=task_name, status=task_status, description=task_description, start_date=task_start_date, due_date=task_due_date, checkboxes=task_checkboxes)
                self.db_handler.update_task(updated_task)
                break

    def remove_task(self, task_item_widget):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget is task_item_widget:
                task_name = widget.label.text()
                self.db_handler.delete_task(task_name)
                self.task_list.takeItem(i)
                break

    def open_edit_window(self, task_item_widget):
        task_name = task_item_widget.label.text()
        task_status = task_item_widget.status_dropdown.currentText()
        task_description = task_item_widget.description
        task_start_date = task_item_widget.start_date
        task_due_date = task_item_widget.due_date
        task_checkboxes = task_item_widget.checkboxes
        task = Task(name=task_name, description=task_description, status=task_status, start_date=task_start_date, due_date=task_due_date, checkboxes=task_checkboxes)

        edit_window = TaskEditWindow(task, self.save_task)
        edit_window.exec_()

    def save_task(self, task):
        self.db_handler.update_task(task)
        self.load_tasks()  # Reload tasks to reflect changes


class TaskItem(QWidget):
    def __init__(self, task_name, update_callback, delete_callback, status="To do", edit_callback=None, description="", start_date="", due_date="", checkboxes=None):
        super().__init__()
        if checkboxes is None:
            checkboxes = []
        self.layout = QHBoxLayout(self)

        self.label = QLabel(task_name, self)
        self.label.mouseDoubleClickEvent = self.open_edit_window  # Set double-click event

        # Status Dropdown
        self.status_dropdown = QComboBox(self)
        self.status_dropdown.addItems(["To do", "On Going", "Done", "Late", "Cancelled"])
        self.status_dropdown.setCurrentText(status)
        self.status_dropdown.currentTextChanged.connect(self.status_changed)

        # Red "X" button for deletion
        self.delete_button = QPushButton("X", self)
        self.delete_button.setStyleSheet("QPushButton {color: red; font-weight: bold; }")
        self.delete_button.setFixedSize(QSize(30, 30))
        self.delete_button.clicked.connect(self.delete_task)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.status_dropdown)
        self.layout.addWidget(self.delete_button)

        self.update_callback = update_callback
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback

        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.checkboxes = checkboxes

    def status_changed(self):
        self.update_callback(self)

    def delete_task(self):
        self.delete_callback(self)

    def open_edit_window(self, event):
        if self.edit_callback:
            self.edit_callback(self)
