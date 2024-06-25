import sqlite3
from database.models import create_tables


def initialize_database():
    conn = sqlite3.connect('task_manager.db')
    create_tables(conn)
    conn.close()
    print("Database initialized successully.")


def seed_database():
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor

    # Add some initial data if needed (e.g., some default users and tasks)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', ''))   # password: admin
    cursor.execute("INSERT INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (1, "Initial Task", "This is a seed task.", "2024-01-01", "2024-01-02", "Not Started", "Subtask 1,Subtask 2"))
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")


if __name__ == "__main__":
    initialize_database()
    seed_database()