from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My Dutch App")
        self.setGeometry(100, 100, 400, 300)

        self.button1 = QPushButton("Next Lesson", self)
        self.button1.move(50, 50)
        self.button1.clicked.connect(self.open_word_window)

        self.button2 = QPushButton("Exam", self)
        self.button2.move(50, 100)
        self.button2.clicked.connect(self.open_window2)

        self.button3 = QPushButton("Verbs", self)
        self.button3.move(50, 150)
        self.button3.clicked.connect(self.open_window3)


    def open_word_window(self):
        self.window = Word_window()
        self.window.show()
        self.hide()

        def handle_counter_changed(value):
            known = value
            print(f"{value} button(s) were clicked.")  # print the final count of clicked buttons

        Word_window.counterChanged.connect(handle_counter_changed)  # connect to the counterChanged signal

        def show_window_2():
            window_check.show()

        window.finished.connect(show_window_2)

    def open_window2(self):
        print('not ready yet')

    def open_window3(self):
        print('not ready yet')

class Word_window(QDialog):
    counterChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1000, 500)  # x, y, width, height
        self.setWindowTitle('Learning Words')
        self.setWindowIcon(QIcon('data_files/python.png'))

        self.counter = 0  # initialize the counter variable

        grid = QGridLayout()
        for i in range(1, 26):
            #btn = QPushButton(f'{sample_of_words[i - 1].getWord()}\n\n{sample_of_words[i - 1].getTranslation()}')
            btn = QPushButton('happiness')
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

class Window_check(QDialog):

    def __init__(self, word):
        super().__init__()

        self.setGeometry(100, 100, 200, 100)  # x, y, width, height
        self.setWindowTitle('Words')

        vbox = QVBoxLayout()

        self.lineedit = QLineEdit()

        # connecting to lineedit
        self.lineedit.editingFinished.connect(self.reply)

        # label for special characters
        self.label = QLabel()
        self.label.setText('Use special characters: [à ë ï é è ç ’]')

        # label for word or translation
        self.label_word = QLabel()
        self.label_word.setText(word)

        vbox.addWidget(self.label)
        vbox.addWidget(self.label_word)
        vbox.addWidget(self.lineedit)
        self.setLayout(vbox)


    def reply(self):
        your_reply = str(self.lineedit.text())
        if your_reply == self.label_word.text():
            print('You are right!')
        else:
            print('Try more!')


app = QApplication(sys.argv)

# setting icon for app
icon = QIcon("data_files/python.png")
app.setWindowIcon(icon)

window = MainWindow()
window.show()



window_check = Window_check('пупок')


sys.exit(app.exec())



