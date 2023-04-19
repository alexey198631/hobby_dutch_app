from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
import sys


class SharedData:
    def __init__(self):
        self.common_list = []

class WindowA(QWidget):
    def __init__(self, shared_data, parent=None):
        super(WindowA, self).__init__(parent)
        self.shared_data = shared_data
        # Access the common list with self.shared_data.common_list

class WindowB(QWidget):
    def __init__(self, shared_data, parent=None):
        super(WindowB, self).__init__(parent)
        self.shared_data = shared_data
        # Access the common list with self.shared_data.common_list

if __name__ == "__main__":
    app = QApplication(sys.argv)

    shared_data = SharedData()

    window_a = WindowA(shared_data)
    window_a.show()

    window_b = WindowB(shared_data)
    window_b.show()

    sys.exit(app.exec())
