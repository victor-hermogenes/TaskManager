import re


def validate_username(username):
    """Validates that the username is at least 3 characters long and contains only alphanumeric characters."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return False, "Username can only contain alphanumeric characters and underscores."
    return True, ""


def validate_password(password):
    """Validates that the password is at least 8 characters long and contains letters and numbers."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search("[a-zA-Z]", password):
        return False, "Password must contain at least one letter."
    if not re.search("[0-9]", password):
        return False, "Password must contain at least one number."
    return True, ""


def validate_task(title, start_date, due_date):
    """Validates that the task title is not empty and dates are in correct order."""
    if not title.strip():
        return False, "Task title cannot be empty."
    if start_date > due_date:
        return False, "Start date cannot be later than due date."
    return True, ""