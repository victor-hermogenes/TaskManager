from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QCheckBox


def format_date(date_str):
    """Converts a date string in 'yyyy-MM-dd' format to a QDate object."""
    year, month, day = map(int, date_str.split('-'))
    return QDate(year, month, day)


def checkboxes_to_list(checkboxes_layout):
    """Extracts checkbox texts from a layout containing QCheckBoxes."""
    checkboxes = []
    for i in range(checkboxes_layout.count()):
        widget = checkboxes_layout.itemAt(i).widget()
        if isinstance(widget, QCheckBox):
            checkboxes.append(widget.text())
    return checkboxes

