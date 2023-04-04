from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
import sys


# object oriented concept
class Window(QWidget):
    counterChanged = pyqtSignal(int)

    def __init__(self, sample_of_words):
        super().__init__()

        self.setGeometry(100, 100, 1000, 500)  # x, y, width, height
        self.setWindowTitle('grid layout')
        self.setWindowIcon(QIcon('data_files/python.png'))

        self.counter = 0  # initialize the counter variable

        grid = QGridLayout()
        for i in range(1, 26):
            btn = QPushButton(f'{sample_of_words[i - 1].getWord()}\n{sample_of_words[i - 1].getTranslation()}')
            btn.setFixedSize(200, 100)
            btn.clicked.connect(self.on_button_clicked)  # connect the clicked signal to a slot
            row = (i - 1) // 5  # calculate the row index
            col = (i - 1) % 5  # calculate the column index
            grid.addWidget(btn, row, col)

        self.setLayout(grid)

    def on_button_clicked(self):
        sender = self.sender()
        if sender.property('clicked'):
            sender.setProperty('clicked', False)
            sender.setStyleSheet("")
            self.counter -= 1
        else:
            sender.setProperty('clicked', True)
            sender.setStyleSheet("background-color: white")  # change the background color of the clicked button
            self.counter += 1

        sender.style().unpolish(sender) # update the button's appearance
        sender.style().polish(sender) # update the button's appearance

    def closeEvent(self, event):
        self.counterChanged.emit(self.counter)  # emit the custom signal with the counter value
        super().closeEvent(event)

"""
app = QApplication(sys.argv)

# setting icon for app
icon = QIcon("data_files/python.png")
app.setWindowIcon(icon)

window = Window()
window.show()
sys.exit(app.exec())"""