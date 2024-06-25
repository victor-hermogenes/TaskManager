import sqlite3


def create_connection():
    conn = sqlite3.connect('task_manager.db')
    return conn


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        start_date TEXT,
        due_date TEXT,
        status TEXT,
        checkboxes TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()


def create_task(user_id, title, description, start_date, due_date, status, checkboxes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, title, description, start_date, due_date, status, ','.join(checkboxes)))
    conn.commit()
    conn.close()

    
def update_task(task_id, title, description, start_date, due_date, status, checkboxes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks SET title = ?, description = ?, start_date = ?, due_date = ?, status = ?, checkboxes = ?
    WHERE id = ?''', (title, description, start_date, due_date, status, ','.join(checkboxes), task_id))
    conn.commit()
    conn.close()

    
def get_tasks_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)

