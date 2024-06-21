from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem


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
            task_item_widget = TaskItem(task_name, self.remove_task)
            task_item = QListWidgetItem(self.task_list)
            task_item.setSizeHint(task_item_widget.sizeHint())
            self.task_list.addItem(task_item)
            self.task_list.setItemWidget(task_item, task_item_widget)
            self.task_input.clear()

    
    def remove_task(self, task_item_widget):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            widget = self.task_list.itemWidget(item)
            if widget is task_item_widget:
                self.task_list.takeItem(i)
                break


class TaskItem(QWidget):
    def __init__(self, task_name, delete_callback):
        super().__init__()
        self.layout = QHBoxLayout(self)

        self.label = QLabel(task_name, self)
        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_task)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.delete_button)

        self.delete_callback = delete_callback

    
    def delete_task(self):
        self.delete_callback(self)