import sys
import pandas as pd
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QWidgetAction)

from PyQt6.QtGui import QAction
from cls import *
from defs import loadWords, random_sample
import random


class ButtonGridWidget(QWidget):
    window_closed = pyqtSignal()
    counterChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        sample = QApplication.instance().shared_object_list
        self.counter = 0  # initialize the counter variable
        grid_layout = QGridLayout()

        for i in range(5):
            for j in range(5):
                button = QPushButton(f'{sample[i * 5 + j].getWord()} \n | \n {sample[i * 5 + j].getTranslation()}', self)
                button.setFixedSize(200, 100)
                #button.clicked.connect(lambda _, x=i, y=j: self.button_clicked(x, y))
                button.clicked.connect(self.on_button_clicked)
                grid_layout.addWidget(button, i, j)

        self.setLayout(grid_layout)

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

        sender.style().unpolish(sender)  # update the button's appearance
        sender.style().polish(sender)  # update the button's appearance

    def closeEvent(self, event):
        self.window_closed.emit()
        self.counterChanged.emit(self.counter)  # emit the custom signal with the counter value
        super().closeEvent(event)

class ButtonGridWidgetSpare(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, list_of_words=[]):
        super().__init__()

        if len(list_of_words) == 0:
            sample = QApplication.instance().shared_object_list
        else:
            sample = list_of_words.copy()
        grid_layout = QGridLayout()


        # change location of each word at the button board
        coord_i = [0, 1, 2, 3, 4]
        coord_j = [0, 1, 2, 3, 4]
        coord = []
        for i in coord_i:
            for j in coord_j:
                coord.append((i, j))
        random.shuffle(coord)
        random.shuffle(sample)

        for k, (i, j) in enumerate(coord):
                try:
                    button = QPushButton(f'{sample[k].getWord()} \n | \n {sample[k].getTranslation()}', self)
                    button.setFixedSize(200, 100)
                    grid_layout.addWidget(button, i, j)
                except:
                    button = QPushButton()
                    button.setFixedSize(200, 100)
                    grid_layout.addWidget(button, i, j)

        self.setLayout(grid_layout)

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

class InputCounterWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, nxt=[]):
        super().__init__()
        if len(nxt) == 0:
            self.list_of_words = QApplication.instance().shared_object_list.copy()
        else:
            self.list_of_words = nxt
        #print([x.getWord() for x in self.list_of_words])

        self.label = QLabel("Enter your translation:", self)
        # label for special characters
        self.label_2 = QLabel('Use special characters: [à ë ï é è ç ’]', self)

        self.temp_label = QLabel()

        self.line_edit = QLineEdit(self)
        self.submit_button = QPushButton("Submit", self)
        self.lcd_counter = QLCDNumber(self)
        self.lcd_counter.setDigitCount(3)
        self.count = 0
        self.indx = 0
        self.list_to_delete = []

        self.submit_button.clicked.connect(self.submit_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label_2)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.line_edit)
        hlayout.addWidget(self.submit_button)
        layout.addLayout(hlayout)

        layout.addWidget(self.lcd_counter)

        layout.addWidget(self.temp_label)

        self.setLayout(layout)

        # Start quiz
        self.next_word()

    def next_word(self):
        #print(self.indx, len(self.list_of_words))
        if self.count == 25:
            self.temp_label.setText("Congrats!")
        elif self.indx == len(self.list_of_words):
            for word in self.list_to_delete:
                self.list_of_words.remove(word)
            self.list_to_delete = []
            self.indx = 0
            self.current_word = self.list_of_words[self.indx]
            self.hideMe()
            self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.list_of_words)
            self.button_grid_window_spare.window_closed.connect(self.shoeMe)
            self.button_grid_window_spare.show()
        else:
            self.current_word = self.list_of_words[self.indx]



        # Set the question label
        self.label.setText(f"{self.current_word.getWord()}: ")

        # Clear the answer line edit and result label
        self.line_edit.clear()


    def submit_text(self):
        text = self.line_edit.text()
        translation = self.current_word.getTranslation()
        if ',' in translation:
            translation = translation.split(',')[0]
        if text == translation:
            self.count += 1
            self.list_to_delete.append(self.current_word)
            self.indx += 1
            self.lcd_counter.display(self.count)
            self.next_word()
        else:
            self.temp_label.setText(f"{self.current_word.getTranslation()}, {len(self.list_of_words)}")
            self.indx += 1
            self.next_word()

    def hideMe(self):
        self.hide()

    def shoeMe(self):
        self.show()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lesson App')
        self.setGeometry(100, 100, 300, 200)

        # File menu and actions
        self.file_menu = self.menuBar().addMenu("File")

        self.show_stat_action = QAction("Show Stat", self)
        self.show_stat_action.triggered.connect(self.show_stat)
        self.file_menu.addAction(self.show_stat_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        next_lesson_btn = QPushButton('Next Lesson', self)
        repeat_btn = QPushButton('Repeat', self)
        exam_btn = QPushButton('Exam', self)

        next_lesson_btn.clicked.connect(self.next_lesson)
        repeat_btn.clicked.connect(self.repeat)
        exam_btn.clicked.connect(self.exam)

        layout = QVBoxLayout()
        layout.addWidget(next_lesson_btn)
        layout.addWidget(repeat_btn)
        layout.addWidget(exam_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_stat(self):
        shared_object_list = QApplication.instance().shared_object_list
        print(f"Shared object list: {shared_object_list}")
        shared_object_list.append("New object")
        print(f"Updated shared object list: {shared_object_list}")


    def next_lesson(self):
        self.button_grid_window = ButtonGridWidget()
        self.button_grid_window.show()
        self.button_grid_window.window_closed.connect(self.open_input_counter_widget)
        self.button_grid_window.counterChanged.connect(self.update_counter)  # connect the signal to the slot
        self.close()

    def open_input_counter_widget(self):
        self.input_counter_widget = InputCounterWidget()
        self.input_counter_widget.show()
        self.input_counter_widget.window_closed.connect(self.show)
        self.close()

    def repeat(self):
        pass

    def exam(self):
        pass

    def update_counter(self, counter_value):
        print(f"Counter value from ButtonGridWidget: {counter_value}")
        # Do something with the counter_value


class CustomApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        words = pd.read_excel('data_files/dutch.xlsx', sheet_name='update')
        words = words.loc[:, 'word':]
        wordList = loadWords(words, "yes")
        sample = random_sample(wordList, 25)

        self.shared_object_list = sample

        lesson_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')
        lesson_df = lesson_df.loc[:, 'lesson':]

        self.lesson = lesson_df


def main():
    app = CustomApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
