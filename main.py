import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db_handler import DBHandler
from models.task import Task


def main():
    app = QApplication(sys.argv)
    
    # Initialize the database handler
    db_handler = DBHandler()

    # Add some test tasks:
    task1 = Task(name="Test Task 1", description="Descripton 1", status="To do")
    db_handler.add_task(task1)

    # Fetch tasks and print them
    tasks = db_handler.get_tasks()
    for task in tasks:
        print(task)
    
    # Close the database connection
    db_handler.close()

    # Initialize and show the main window
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()