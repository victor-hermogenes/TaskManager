import sqlite3


class DBHandler:
    def __init__(self, db_name='tasks.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTERGER PRIMARY KEY.
                name TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL                
            )
        """)
        self.connection.commit()


    def add_task(self, task):
        self.cursor.execute("INSERT INTO tasks (name, description, status) VALUES (?, ?, ?)",
                            (task.name, task.description, task.status))
        self.connection.commit()
    

    def get_tasks(self):
        self.cursor.execute("SELECT name, description, status FROM tasks")
        tasks = self.cursos.fetchall()
        return [Task(name, description, status) for name, description, status in tasks]
    

    def close(self):
        self.connection.close()