def apply_light_mode(app):
    light_stylesheet = """
    QWidget {
        background-color: #ffffff;
        color: #000000;
        font-size: 14px;
    }
    QMenuBar {
        background-color: #ffffff;
    }
    QMenuBar::item {
        background-color: #ffffff;
        color: #000000;
    }
    QMenuBar::item:selected{
        background-color: #F0F0F0
    }
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #DDDDDD;
        padding: 5px;
        border-radius: 5px;
        color: #000000
    }
    QPushButton:hover {
        background-color: #D3D3D3;
    }
    QLineEdit, QComboBox, QDateEdit, QTextEdit {
        background-color: #F8F8F8;
        border: 1px solid #DDDDDD;
        color: #000000;
        padding: 5px;
        border-radius: 5px;
    }
    QLineEdite:disabled, QComboBox:disabled, QDateEdit:disabled, QTextEdit:disabled {
        color: #AAAAAA
    }
    """

    app.setStyleSheet(light_stylesheet)