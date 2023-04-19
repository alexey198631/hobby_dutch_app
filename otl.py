from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
import sys


class TestWindow(QDialog):


    def __init__(self, word):
        super().__init__()

        self.setGeometry(100, 100, 200, 100)  # x, y, width, height
        self.setWindowTitle('Test Window')

        vbox = QVBoxLayout()

        self.lineedit = QLineEdit()

        # connecting to lineedit
        #self.lineedit.editingFinished.connect(self.reply)

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

        # Connect the returnPressed signal of the line edit widget to the on_return_pressed function
        self.line_edit.returnPressed.connect(self.on_return_pressed)

        # Start the quiz
        self.next_word()

    def right_word(self, word, translation, rever=0):
        point_counter = 0
        if rever == 1:
            while True:
                self.label.setText(f'\nPress "1","2","3" to open 1, 2, 3 letters in the word\n\n {translation}: ')
                if x == word:
                    return [True, point_counter]
                elif x == '1' or x == '2' or x == '3':
                    print(help_for_guess(word, int(x)))
                    point_counter += int(x)
                else:
                    return [False, point_counter]

        elif rever == 0:
            translation = translation_with_comma(translation)
            while True:
                x = input(f'\nPress "1","2","3" to open 1, 2, 3 letters in the word\n\n {word}: ')
                if x in translation:
                    return [True, point_counter]
                elif x == '1' or x == '2' or x == '3':
                    print(help_for_guess(translation[0], int(x)))
                    point_counter += int(x)
                else:
                    return [False, point_counter]

    def cycle(sample_of_words, rever):
        p = 250
        s = sample_of_words.copy()
        while len(s) > 0:
            random.shuffle(s)
            lst_to_delete = []
            for i in s:
                temp = right_word(i.getWord(), i.getTranslation(), rever)
                if temp[0]:
                    print("\nRIGHT!")
                    p = p - temp[1]
                    i.addSuccess()
                    if rever == 0:
                        i.addTrials_d()
                    else:
                        i.addTrials_r()
                    lst_to_delete.append(i)
                else:
                    print("\nWRONG!")
                    p = p - temp[1]
                    p -= 1
                    if rever == 0:
                        i.addTrials_d()
                    else:
                        i.addTrials_r()
            if len(lst_to_delete) > 0:
                for w in lst_to_delete:
                    s.remove(w)
                if len(s) != 0:
                    plotting(s)
            else:
                if len(s) != 0:
                    plotting(s)
        print(p, '\n')
        return p

app = QApplication(sys.argv)

# setting icon for app
icon = QIcon("data_files/python.png")
app.setWindowIcon(icon)

window = TestWindow('Привет')
window.show()
sys.exit(app.exec())