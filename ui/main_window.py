from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from ui.task_view import TaskView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.task_view = TaskView()
        self.layout.addWidget(self.task_view)