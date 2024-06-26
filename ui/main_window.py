import sys
import os

# Ensure the directory containing the 'task_card' module is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QMenuBar, QAction, QPushButton, QScrollBar
from task_card import TaskCard
from dark_mode import apply_dark_mode
from light_mode import apply_light_mode
from tasks.create_task import CreateTaskWindow
from tasks.edit_task import EditTaskWindow
from database.models import get_tasks_by_user, get_user_id_by_username

CONFIG_FILE = 'config.txt'

TASKS_BATCH_SIZE = 10


def save_style_preference(style):
    with open(CONFIG_FILE, 'w') as f:
        f.write(style)


class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_id = get_user_id_by_username(username)
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)
        self.tasks_offset = 0
        self.tasks_loaded = False
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")
        
        light_mode_action = QAction("Light Mode", self)
        dark_mode_action = QAction("Dark Mode", self)
        
        light_mode_action.triggered.connect(self.set_light_mode)
        dark_mode_action.triggered.connect(self.set_dark_mode)
        
        view_menu.addAction(light_mode_action)
        view_menu.addAction(dark_mode_action)

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.show_create_task_window)
        layout.addWidget(self.add_task_button)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_container.setLayout(self.task_layout)
        self.scroll.setWidget(self.task_container)
        self.scroll.verticalScrollBar().valueChanged.connect(self.on_scroll)

        layout.addWidget(self.scroll)

        layout.setStretch(1, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.load_tasks()

    def set_light_mode(self):
        apply_light_mode(QApplication.instance())
        save_style_preference('light')
    

    def set_dark_mode(self):
        apply_dark_mode(QApplication.instance())
        save_style_preference('dark')


    def show_create_task_window(self):
        self.create_task_window = CreateTaskWindow(self.user_id)
        self.create_task_window.task_created.connect(self.load_tasks)
        self.create_task_window.show()


    def load_tasks(self):
        tasks = get_tasks_by_user(self.user_id, self.tasks_offset, TASKS_BATCH_SIZE)
        if tasks:
            self.tasks_offset += len(tasks)
            for task in tasks:
                task_card = TaskCard(task)
                task_card.edit_requested.connect(self.show_edit_task_window)
                self.task_layout.addWidget(task_card)
        else:
            self.tasks_loaded = True

    
    def reload_tasks(self):
        self.tasks_offset = 0
        self.tasks_loaded = False
        self.clear_tasks()
        self.load_tasks()

    
    def clear_tasks(self):
        for i in reversed(range(self.task_layout.count())):
            widget = self.task_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)


    def show_edit_task_window(self, task):
        self.edit_task_window = EditTaskWindow(task)
        self.edit_task_window.task_updated.connect(self.load_tasks)
        self.edit_task_window.show()

    
    def on_scroll(self):
        if not self.tasks_loaded and self.scroll.verticalScrollBar().value() >= self.scroll.verticalScrollBar().maximum() - 50:
            self.load_tasks()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow('admin')  # Replace with actual username if needed
    window.show()
    sys.exit(app.exec_())