class Task:
    def __init__(self, id=None, name='', description='', status='Pending', start_date='', due_date='', checkboxes=[]):
        self.id = id
        self.name = name
        self.description = description
        self.status = status
        self.start_date = start_date
        self.due_date = due_date
        self.checkboxes = checkboxes

    def __str__(self):
        return f"{self.name}: {self.description} - {self.status} (Start: {self.start_date}, Due: {self.due_date})"
