import sqlite3
import sys
import os

# Ensure the directory containing the 'database' package is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import create_tables  # Adjusted import

def initialize_database():
    conn = sqlite3.connect('task_manager.db')
    create_tables(conn)
    conn.close()
    print("Database initialized successfully.")

def seed_database():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    # Add some initial data if needed (e.g., some default users and tasks)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', '$2b$12$KIXr.bkqJxZtEp/yTjD0uOAfkV4dHRihAwzE6LBZIXakmgTQa4YAe'))  # password: admin
    cursor.execute("INSERT INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (1, "Initial Task", "This is a seed task.", "2024-01-01", "2024-01-02", "Not Started", "Subtask 1,Subtask 2"))

    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    initialize_database()
    seed_database()