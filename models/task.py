class Task:
    def __init__(self, name, description='', status='To do'):
        self.name = name
        self.description = description
        self.status = status
    

    def __str__(self):
        return f"{self.name}: {self.description} - {self.status}"
    