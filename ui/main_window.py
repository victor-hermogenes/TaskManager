from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QMenuBar, QAction
import sys
from task_card import TaskCard
from dark_mode import apply_dark_mode
from light_mode import apply_light_mode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        # menu bar for light/dark mode
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")

        light_mode_action = QAction("Light Mode", self)
        dark_mode_action = QAction("Dark Mode", self)

        light_mode_action.triggered.connect(self.set_light_mode)
        dark_mode_action.triggered.connect(self.set_dark_mode)

        view_menu.addAction(light_mode_action)
        view_menu.addAction(dark_mode_action)
        
        # Scroll area for tasks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        task_container = QWidget()
        task_layout = QVBoxLayout

        # Sample task data
        task_id = 1
        title = "Sample Task"
        description = "This is a description of the sample task."
        start_date = "2024-06-24"
        due_date = "2024-07-01"
        status = "In Progress"
        checkboxes = ["Subtask 1", "Subtask 2", "Subtask 3"]

        # Create and add task card to layout
        task_card = TaskCard(task_card)

        task_container.setLayout(task_layout)
        scroll.setWidget(task_container)

        layout.addWidget(scroll)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    
    def set_light_mode(self):
        apply_light_mode(QApplication.instance())
        apply_dark_mode(QApplication.instance())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())