import sqlite3
from models.task import Task


class DBHandler:
    def __init__(self, db_name='tasks.db'):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_table()
            print(f"Databe {db_name} conneted successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    
    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")


    def add_task(self, task):
        try:
            self.cursor.execute("INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)",
                                (task.name, task.description, task.status))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")
    

    def get_tasks(self):
        try:
            self.cursor.execute("SELECT name, description, status FROM tasks")
            tasks = self.cursor.fetchall()
            return [Task(name, description, status) for name, description, status in tasks]
        except sqlite3.Error as e:
            print(f"Error retrieving tasks: {e}")
    

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")
        

# Test the database handler
if __name__ == "__main__":
    db_handler = DBHandler()
    task1 = Task(name="Test Task 1", description="Description 1", status="To do")
    db_handler.add_task(task1)
    tasks = db_handler.get_tasks()
    for task in tasks:
        print(task)
    db_handler.close()