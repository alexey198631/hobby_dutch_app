from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QMainWindow, QDialog, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from random import shuffle
import sys

class MainWindow(QMainWindow):
    def __init__(self, sample_of_words):
        super().__init__()

        self.setWindowTitle("My Dutch App")
        self.setGeometry(100, 100, 400, 300)

        self.button1 = QPushButton("Next Lesson", self)
        self.button1.move(50, 50)
        self.button1.clicked.connect(self.open_word_window(sample_of_words))

        self.button2 = QPushButton("Exam", self)
        self.button2.move(50, 100)
        self.button2.clicked.connect(self.open_window2)

        self.button3 = QPushButton("Verbs", self)
        self.button3.move(50, 150)
        self.button3.clicked.connect(self.open_window3)


    def open_word_window(self, sample):
        self.window = Word_window(sample)
        self.window.show()
        self.hide()

    def open_window2(self):
        print('not ready yet')

    def open_window3(self):
        print('not ready yet')

class Word_window(QDialog):
    counterChanged = pyqtSignal(int)

    def __init__(self, sample_of_words):
        super().__init__()

        self.setGeometry(100, 100, 1000, 500)  # x, y, width, height
        self.setWindowTitle('Learning Words')
        self.setWindowIcon(QIcon('data_files/python.png'))

        self.counter = 0  # initialize the counter variable
        self.sample = sample_of_words

        grid = QGridLayout()
        for i in range(1, 26):
            btn = QPushButton(f'{sample_of_words[i - 1].getWord()}\n\n{sample_of_words[i - 1].getTranslation()}')
            btn.setFixedSize(200, 100)
            btn.clicked.connect(self.on_button_clicked)  # connect the clicked signal to a slot
            row = (i - 1) // 5  # calculate the row index
            col = (i - 1) % 5  # calculate the column index
            grid.addWidget(btn, row, col)

        self.setLayout(grid)

        # connect the finished signal to a slot that will create and show the new widget window
        self.finished.connect(self.show_new_window)

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

    def show_new_window(self):
        # create the new widget window
        new_window = QuizWindow(self.sample)

        # show the new widget window
        new_window.show()

class Window_2(QDialog):

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

class QuizWindow(QWidget):
    def __init__(self, list_of_words):
        super().__init__()

        self.setWindowTitle("Dictionary Quiz")

        # Save the list of words as a class attribute
        self.lesson_words = list_of_words

        # Create a label, line edit widgets
        self.label = QLabel()
        self.line_edit = QLineEdit()

        # Create a vertical layout
        vbox = QVBoxLayout()

        # Add the label, line edit  widgets to the layout
        vbox.addWidget(self.label)
        vbox.addWidget(self.line_edit)

        # Set the layout for the main window
        self.setLayout(vbox)

        # Connect the returnPressed signal of the line edit widget to the on_return_pressed function
        self.line_edit.editingFinished.connect(self.on_return_pressed)

        # Initialize the score and attempt counters
        self.score = 0
        self.attempts = 0

        # Start the quiz
        self.next_word()

    def next_word(self):
        self.sample = self.lesson_words.copy()
        if len(self.sample) > 0 and not self.attempts == 25:

            # Shuffle the words in a list not to remember them by order
            shuffle(self.sample)
            print(self.sample)

            # Get the next word and translation from the list of words
            self.current = self.sample[-1]
            self.current_word = self.sample[-1].getWord()
            self.current_translation = self.sample[-1].getTranslation()

            # Set the label text to the current word
            self.label.setText(self.current_word)

            # Clear the line edit text
            self.line_edit.setText("")
        else:
            QMessageBox.information(self, 'Lesson Success', f"You answered {self.score} words for {self.attempts} attempts.")
            sys.exit()

    def on_return_pressed(self):
        # Get the text from the line edit widget
        translation = self.line_edit.text()

        # Increment the attempt counter
        self.attempts += 1
        self.current.addTrials_d()

        # Check if the translation is correct
        if translation.lower() == self.current_translation.lower():
            print('I am here', self.current)
            self.score += 1
            self.current.addSuccess()
            # Remove the word from the sample if the translation is correct
            self.sample.remove(self.current)
            # Go to the next word
        self.next_word()



"""

app = QApplication(sys.argv)

# setting icon for app
icon = QIcon("data_files/python.png")
app.setWindowIcon(icon)

window = Window()
window.show()
sys.exit(app.exec())"""