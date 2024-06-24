import sqlite3
from models.task import Task

class DBHandler:
    def __init__(self, db_name='tasks.db'):
        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_table()
            print(f"Database {db_name} connected successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    start_date TEXT,
                    due_date TEXT,
                    checkboxes TEXT
                )
            ''')
            self.connection.commit()
            print("Table 'tasks' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def add_task(self, task):
        try:
            self.cursor.execute("INSERT INTO tasks (name, description, status, start_date, due_date, checkboxes) VALUES (?, ?, ?, ?, ?, ?)",
                                (task.name, task.description, task.status, task.start_date, task.due_date, str(task.checkboxes)))
            self.connection.commit()
            task.id = self.cursor.lastrowid  # Get the last inserted row ID
            print(f"Task '{task.name}' added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")

    def update_task(self, task):
        try:
            self.cursor.execute("UPDATE tasks SET name = ?, description = ?, status = ?, start_date = ?, due_date = ?, checkboxes = ? WHERE id = ?",
                                (task.name, task.description, task.status, task.start_date, task.due_date, str(task.checkboxes), task.id))
            self.connection.commit()
            print(f"Task '{task.name}' updated successfully.")
        except sqlite3.Error as e:
            print(f"Error updating task: {e}")

    def delete_task(self, task_name):
        try:
            self.cursor.execute("DELETE FROM tasks WHERE name = ?", (task_name,))
            self.connection.commit()
            print(f"Task '{task_name}' deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting task: {e}")

    def get_tasks(self):
        try:
            self.cursor.execute("SELECT id, name, description, status, start_date, due_date, checkboxes FROM tasks")
            tasks = self.cursor.fetchall()
            return [Task(id, name, description, status, start_date, due_date, eval(checkboxes)) for id, name, description, status, start_date, due_date, checkboxes in tasks]
        except sqlite3.Error as e:
            print(f"Error retrieving tasks: {e}")
            return []

    def close(self):
        try:
            self.connection.close()
            print("Database connection closed successfully.")
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")
