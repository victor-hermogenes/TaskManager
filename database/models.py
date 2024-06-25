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
        assigned_user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(assigned_user_id) REFERENCES users(id)
    )''')
    conn.commit()


def add_assigned_user_column(conn):
    cursor = conn.cursor()
    try:
        cursor.execute('ALTER TABLE tasks ADD COLUMN assigned_user_id INTEGER')
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass


def initialize_database():
    conn = create_connection()
    create_tables(conn)
    add_assigned_user_column(conn)  # Ensure the column exists
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
    INSERT OR IGNORE INTO tasks (user_id, assigned_user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES ((SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM users WHERE username = 'user1'), 'Initial Task 1', 'Description for initial task 1', '2024-01-01', '2024-01-10', 'Not Started', 'Subtask 1,Subtask 2')
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO tasks (user_id, assigned_user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES ((SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM users WHERE username = 'user2'), 'Initial Task 2', 'Description for initial task 2', '2024-01-02', '2024-01-11', 'In Progress', 'Subtask 1,Subtask 2')
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


def create_task(user_id, assigned_user_id, title, description, start_date, due_date, status, checkboxes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tasks (user_id, assigned_user_id, title, description, start_date, due_date, status, checkboxes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (user_id, assigned_user_id, title, description, start_date, due_date, status, ','.join(checkboxes)))
    conn.commit()
    conn.close()


def update_task(task_id, assigned_user_id, title, description, start_date, due_date, status, checkboxes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tasks SET assigned_user_id = ?, title = ?, description = ?, start_date = ?, due_date = ?, status = ?, checkboxes = ?
    WHERE id = ?''', (assigned_user_id, title, description, start_date, due_date, status, ','.join(checkboxes), task_id))
    conn.commit()
    conn.close()


def get_tasks_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ? OR assigned_user_id = ?', (user_id, user_id))
    tasks = cursor.fetchall()
    conn.close()
    return tasks