def apply_dark_mode(app):
    dark_stylesheet = """
    QWidget {
        background-color: #2d2d2d;
        color: #d3d3d3;
        font-size: 14px;
    }
    QMenuBar {
        background-color: #2d2d2d;
    }
    QMenuBar::item {
        background-color: #2d2d2d;
        color: #d3d3d3;
    }
    QMenuBar::item:selected{
        background-color: #333333
    }
    QPushButton {
        background-color: #3d3d3d;
        border: 1px solid #5d5d5d;
        padding: 5px;
        border-radius: 5px;
        color: #FFFFFF
    }
    QPushButton:hover {
        background-color: #5d5d5d;
    }
    QLineEdit, QComboBox, QDateEdit, QTextEdit {
        background-color: #3d3d3d;
        border: 1px solid #5d5d5d;
        color: #d3d3d3;
        padding: 5px;
        border-radius: 5px;
    }
    QLineEdite:disabled, QComboBox:disabled, QDateEdit:disabled, QTextEdit:disabled {
        color: #555555;
    }
    """

    app.setStyleSheet(dark_stylesheet)