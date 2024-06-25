import sys
import os

# Ensure the directory containing the 'task_card' module is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QMenuBar, QAction, QPushButton
import sys
from task_card import TaskCard
from dark_mode import apply_dark_mode
from light_mode import apply_light_mode
from tasks.create_task import CreateTaskWindow
from database.models import get_tasks_by_user, get_user_id_by_username


class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_id = get_user_id_by_username(username)  # Fetch the user ID based on the username
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        # Menu bar for light/dark mode
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")
        
        light_mode_action = QAction("Light Mode", self)
        dark_mode_action = QAction("Dark Mode", self)
        
        light_mode_action.triggered.connect(self.set_light_mode)
        dark_mode_action.triggered.connect(self.set_dark_mode)
        
        view_menu.addAction(light_mode_action)
        view_menu.addAction(dark_mode_action)

        # Add Task Button
        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.show_create_task_window)
        layout.addWidget(self.add_task_button)

        # Scroll area for tasks
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_container.setLayout(self.task_layout)
        self.scroll.setWidget(self.task_container)
        layout.addWidget(self.scroll)

        self.load_tasks()

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


    def set_light_mode(self):
        apply_light_mode(QApplication.instance())
    

    def set_dark_mode(self):
        apply_dark_mode(QApplication.instance())


    def show_create_task_window(self):
        self.create_task_window = CreateTaskWindow(self.user_id)
        self.create_task_window.show()
        self.create_task_window.destroyed.connect(self.load_tasks)  # Refresh task list after creating a new task


    def load_tasks(self):
        # Clear current tasks
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Load tasks from the database
        tasks = get_tasks_by_user(self.user_id)
        for task in tasks:
            task_card = TaskCard(task)
            self.task_layout.addWidget(task_card)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    user_id = 1  # Placeholder for logged in user
    window = MainWindow(user_id)
    window.show()
    sys.exit(app.exec_())