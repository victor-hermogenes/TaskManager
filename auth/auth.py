import bcrypt
import sqlite3


def get_db_connection():
    conn = sqlite3.connect('task_manager.db')
    return conn


def register_user(username, password, role='user'):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        return False    # Username already exists
    finally:
        conn.close()
    return True


def login_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return False, None    # User not found
    
    stored_password, role = result
    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        return True, role
    else:
        return False, None