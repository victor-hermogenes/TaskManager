from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    finished = pyqtSignal(bool)
    result = pyqtSignal(bool)


    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs


    @pyqtSlot()
    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.result.emit(result)
        self.finished.emit(True)