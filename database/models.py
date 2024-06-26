import sqlite3
import bcrypt


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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_assignees (
        task_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY(task_id) REFERENCES tasks(id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        PRIMARY KEY (task_id, user_id)
    )''')

    conn.commit()


def initialize_database():
    conn = create_connection()
    create_tables(conn)
    conn.close()
    print("Database initialized successfully.")


def seed_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Add some initial users
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())))
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('user1', bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt())))
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('user2', bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt())))

    # Add some initial tasks
    cursor.execute('''
    INSERT OR IGNORE INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES ((SELECT id FROM users WHERE username = 'admin'), 'Initial Task 1', 'Description for initial task 1', '2024-01-01', '2024-01-10', 'Not Started', 'Subtask 1,Subtask 2')
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES ((SELECT id FROM users WHERE username = 'admin'), 'Initial Task 2', 'Description for initial task 2', '2024-01-02', '2024-01-11', 'In Progress', 'Subtask 1,Subtask 2')
    ''')

    # Assign users to tasks
    cursor.execute('''
    INSERT OR IGNORE INTO task_assignees (task_id, user_id)
    VALUES ((SELECT id FROM tasks WHERE title = 'Initial Task 1'), (SELECT id FROM users WHERE username = 'user1'))
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO task_assignees (task_id, user_id)
    VALUES ((SELECT id FROM tasks WHERE title = 'Initial Task 2'), (SELECT id FROM users WHERE username = 'user2'))
    ''')

    conn.commit()
    conn.close()
    print("Database seeded successfully.")


def get_user_id_by_username(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]
    conn.close()
    return user_id


def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def create_task(user_id, title, description, start_date, due_date, status, checkboxes, assignees):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, title, description, start_date, due_date, status, ','.join(checkboxes)))
    task_id = cursor.lastrowid

    for assignee in assignees:
        cursor.execute('''
        INSERT INTO task_assignees (task_id, user_id)
        VALUES (?, ?)''', (task_id, assignee))

    conn.commit()
    conn.close()


def update_task(task_id, title, description, start_date, due_date, status, checkboxes, assignees):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks SET title = ?, description = ?, start_date = ?, due_date = ?, status = ?, checkboxes = ?
    WHERE id = ?''', (title, description, start_date, due_date, status, ','.join(checkboxes), task_id))

    cursor.execute('DELETE FROM task_assignees WHERE task_id = ?', (task_id,))
    for assignee in assignees:
        cursor.execute('''
        INSERT INTO task_assignees (task_id, user_id)
        VALUES (?, ?)''', (task_id, assignee))

    conn.commit()
    conn.close()


def get_tasks_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT tasks.* FROM tasks
    LEFT JOIN task_assignees ON tasks.id = task_assignees.task_id
    WHERE tasks.user_id = ? OR task_assignees.user_id = ?
    GROUP BY tasks.id
    ''', (user_id, user_id))
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def get_assignees_by_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT users.id, users.username FROM users
    JOIN task_assignees ON users.id = task_assignees.user_id
    WHERE task_assignees.task_id = ?
    ''', (task_id,))
    assignees = cursor.fetchall()
    conn.close()
    return assignees