from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QCheckBox, QWidget
from PyQt5.QtCore import QDate

class TaskEditWindow(QDialog):
    def __init__(self, task, save_callback):
        super().__init__()
        self.task = task
        self.save_callback = save_callback

        self.setWindowTitle("Edit Task")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout(self)

        self.name_label = QLabel("Task Name:")
        self.name_input = QLineEdit(self)
        self.name_input.setText(self.task.name)

        self.description_label = QLabel("Description:")
        self.description_input = QLineEdit(self)
        self.description_input.setText(self.task.description)

        self.start_date_label = QLabel("Start Date:")
        self.start_date_input = QDateEdit(self)
        self.start_date_input.setDate(QDate.currentDate())

        self.due_date_label = QLabel("Due Date:")
        self.due_date_input = QDateEdit(self)
        self.due_date_input.setDate(QDate.currentDate())

        self.checkboxes = []
        self.add_checkbox("Checkbox 1")
        self.add_checkbox("Checkbox 2")

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_task)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_input)
        layout.addWidget(self.due_date_label)
        layout.addWidget(self.due_date_input)
        layout.addStretch()

        for checkbox in self.checkboxes:
            layout.addWidget(checkbox["widget"])

        layout.addWidget(self.save_button)

    def add_checkbox(self, label_text):
        checkbox_widget = QWidget(self)
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox = QCheckBox(self)
        checkbox_label = QLineEdit(self)
        checkbox_label.setText(label_text)
        checkbox_layout.addWidget(checkbox)
        checkbox_layout.addWidget(checkbox_label)
        self.checkboxes.append({"widget": checkbox_widget, "checkbox": checkbox, "label": checkbox_label})

    def save_task(self):
        self.task.name = self.name_input.text()
        self.task.description = self.description_input.text()
        self.task.start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        self.task.due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        self.task.checkboxes = [(cb["checkbox"].isChecked(), cb["label"].text()) for cb in self.checkboxes]
        print(f"Saving task with ID {self.task.id}")  # Debug print
        self.save_callback(self.task)
        self.accept()


