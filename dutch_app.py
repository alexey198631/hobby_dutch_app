"""
translation correct not only for the first part



"""
import sys
import pandas as pd
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QGroupBox)

from PyQt6.QtGui import QAction
from defs import loadWords, random_sample, translation_with_comma
import random


class ButtonGridWidget(QWidget):
    window_closed = pyqtSignal()
    counterChanged = pyqtSignal(int)
    sampleList = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        words = pd.read_excel('data_files/dutch.xlsx', sheet_name='update')
        words = words.loc[:, 'word':]
        wordList = loadWords(words, "yes")
        sample = random_sample(wordList, 25)

        self.shared_object_list = sample

        lesson_df = pd.read_excel('data_files/dutch.xlsx', sheet_name='lesson')
        lesson_df = lesson_df.loc[:, 'lesson':]

        self.lesson = lesson_df


        self.counter = 0  # initialize the counter variable
        grid_layout = QGridLayout()

        for i in range(5):
            for j in range(5):
                button = QPushButton(f'{sample[i * 5 + j].getWord()} \n | \n {sample[i * 5 + j].getTranslation()}',
                                     self)
                button.setFixedSize(200, 100)
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
        self.sampleList.emit(self.shared_object_list) # emit sample of words
        super().closeEvent(event)


class ButtonGridWidgetSpare(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, list_of_words=[], rever=0):
        super().__init__()

        self.rever = rever
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
                if self.rever == 0:
                    button = QPushButton(f'{sample[k].getWord()} \n | \n {sample[k].getTranslation()}', self)
                    button.setFixedSize(200, 100)
                    grid_layout.addWidget(button, i, j)
                elif self.rever == 1:
                    button = QPushButton(f'{sample[k].getTranslation()} \n | \n {sample[k].getWord()}', self)
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

    def __init__(self, main_window, sampleList, nxt=[], rever=0):
        super().__init__()
        if len(nxt) == 0:
            self.list_of_words = sampleList.copy()
        else:
            self.list_of_words = nxt

        self.rever = rever
        self.main_window = main_window
        self.start_list = sampleList.copy()
        self.label = QLabel("Enter your translation:", self)
        self.temp_label = QLabel()
        self.line_edit = QLineEdit(self)
        self.submit_button = QPushButton("Submit", self)
        self.lcd_counter = QLCDNumber(self)
        self.lcd_counter.setDigitCount(3)
        self.count = 0
        self.indx = 0
        self.list_to_delete = []

        self.submit_button.clicked.connect(self.submit_text)
        self.line_edit.returnPressed.connect(self.submit_button.click)

        # Create QGroupBox for special character buttons
        groupBox = QGroupBox('Special Characters', self)
        hbox = QHBoxLayout(groupBox)

        # Create buttons with special characters
        spec_buttons = ['à', 'ë', 'ï', 'é', 'è', 'ç', '’']
        for char in spec_buttons:
            button = QPushButton(char, self)
            button.clicked.connect(lambda _, ch=char: self.insertChar(ch))
            hbox.addWidget(button)

        # Vertical layout with label for words/translations
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # Horizontal layout with line_edit and submit button under the words/translation label
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.line_edit)
        hlayout.addWidget(self.submit_button)
        layout.addLayout(hlayout)
        layout.addWidget(self.lcd_counter)
        layout.addWidget(self.temp_label)
        layout.addWidget(groupBox)
        self.setLayout(layout)

        # Start quiz
        self.next_word()

    def next_word(self):
        if self.count == 25 and self.rever == 0:
            self.rever = 1
            self.list_to_delete = []
            self.start_translation()
        elif self.count == 25 and self.rever == 1:
            self.close()
        elif self.indx == len(self.list_of_words):
            for word in self.list_to_delete:
                self.list_of_words.remove(word)
            self.list_to_delete = []
            self.indx = 0
            self.current_word = self.list_of_words[self.indx]
            self.hideMe()
            self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.list_of_words)
            self.button_grid_window_spare.move(100, 100)
            self.button_grid_window_spare.window_closed.connect(self.shoeMe)
            self.button_grid_window_spare.show()
        else:
            self.current_word = self.list_of_words[self.indx]

        # Set the question label
        if self.rever == 0:
            self.label.setText(f"{self.current_word.getWord()}: ")
        elif self.rever == 1:
            self.label.setText(f"{self.current_word.getTranslation()}: ")

        # Clear the answer line edit and result label
        self.line_edit.clear()

    def submit_text(self):
        text = self.line_edit.text()
        if self.rever == 0:
            translation = self.current_word.getTranslation()
        elif self.rever == 1:
            translation = self.current_word.getWord()
        translation = translation_with_comma(translation) # create list of all translations 
        if text in translation:
            self.count += 1
            self.list_to_delete.append(self.current_word)
            self.indx += 1
            self.lcd_counter.display(self.count)
            self.next_word()
        else:
            self.temp_label.setText(f"{self.current_word.getWord()}, {self.current_word.getTranslation()}")
            self.indx += 1
            self.next_word()

    def hideMe(self):
        self.hide()

    def shoeMe(self):
        self.show()

    def insertChar(self, ch):
        # Insert character into QLineEdit
        self.line_edit.insert(ch)

    def start_translation(self):
        self.close()
        self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.start_list)
        self.button_grid_window_spare.move(100, 100)
        self.button_grid_window_spare.window_closed.connect(self.open_tranlsation_counter_widget)
        self.button_grid_window_spare.show()

    def open_tranlsation_counter_widget(self):
        self.input_translation_widget = InputCounterWidget(self, self.start_list, rever=1)
        self.input_translation_widget.move(100, 100)
        self.input_translation_widget.show()
        self.input_translation_widget.window_closed.connect(self.main_window_back)

    def main_window_back(self):
        self.main_window.show()

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
        self.button_grid_window.move(100, 100)
        self.button_grid_window.show()
        self.button_grid_window.sampleList.connect(self.open_input_counter_widget)
        self.button_grid_window.counterChanged.connect(self.update_counter)  # connect the signal to the slot
        self.hide()

    def open_input_counter_widget(self, sampleList):
        self.input_counter_widget = InputCounterWidget(self, sampleList)
        self.input_counter_widget.move(100, 100)
        self.input_counter_widget.show()

    def repeat(self):
        pass

    def exam(self):
        pass

    def update_counter(self, counter_value):
        print(f"Counter value from ButtonGridWidget: {counter_value}")
        # Do something with the counter_value


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    main_window = MainWindow()
    main_window.move(100, 100)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()