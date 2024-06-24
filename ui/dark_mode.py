import qdarkstyle

def apply_dark_mode(app):
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())