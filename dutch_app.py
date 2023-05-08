"""
To do:

window with words and its translation for speaking lesson
exam mode
verbs mode
separate lcd for score and attempts
two languages databases
if now db?? I need to create the initial start version



"""
import sys
import pandas as pd
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QGroupBox, QListWidget, QTableWidget, QTableWidgetItem)

from PyQt6.QtGui import QAction
from defs import *
import random
import sqlite3


class TextWindow(QMainWindow):
    def __init__(self, main_window, data=None):
        super().__init__()

        self.main_window = main_window

        # Set the fixed size of the window
        self.setFixedSize(350, 380)

        # Create a widget to hold the table and text input field
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Create a table widget and add it to the layout
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Set the column widths
        self.table_widget.setColumnWidth(0, 400)  # Set the width of the first column to 200 pixels
        self.table_widget.setColumnWidth(1, 200)  # Set the width of the second column to 100 pixels
        self.table_widget.setColumnWidth(2, 200)  # Set the width of the second column to 100 pixels

        # Set the column names
        column_names = list(data.columns)
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # If data is provided, populate the table with the data
        if data is not None:
            self.populate_table(data)

        # Create a button to go to Main Menu
        submit_button = QPushButton("Main Menu")
        submit_button.clicked.connect(self.main_window_back)
        layout.addWidget(submit_button)

        # Set the central widget of the window to the input widget
        self.setCentralWidget(widget)

        # Resize the columns and rows to fit the content
        #self.table_widget.resizeColumnsToContents()
        #self.table_widget.resizeRowsToContents()

        # Initialize the sort order for each column to None
        self.sort_order = [None] * self.table_widget.columnCount()

        # Connect the sectionClicked signal to the sort_table function
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)

    def populate_table(self, data):
        # Convert the DataFrame to a list of lists
        table_data = data.values.tolist()

        # Set the number of rows and columns in the table
        self.table_widget.setRowCount(len(table_data))
        self.table_widget.setColumnCount(len(table_data[0]))

        # Populate the table with the data
        for i, row in enumerate(table_data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if j != 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Set the text alignment of the cell to center
                    item.setData(Qt.ItemDataRole.DisplayRole, float(val))  # Set the data type of the cell to float
                self.table_widget.setItem(i, j, item)

    def sort_table(self, logical_index):
        # Get the current sort order for the column
        current_order = self.sort_order[logical_index]

        # Determine the new sort order for the column
        if current_order is None or current_order == Qt.SortOrder.DescendingOrder:
            new_order = Qt.SortOrder.AscendingOrder
        else:
            new_order = Qt.SortOrder.DescendingOrder

        # Sort the table in the desired order
        self.table_widget.sortItems(logical_index, new_order)

        # Update the sort order for the column
        self.sort_order[logical_index] = new_order

    def main_window_back(self):
        self.close()
        self.main_window.show()

class RepeatWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setGeometry(100, 100, 800, 400)  # x, y, width, height
        self.setWindowTitle('Lessons to repeat')

        conn2 = sqlite3.connect('data_files/lessons.db')
        df = pd.read_sql('SELECT * FROM lessons', conn2)
        lesson_df = df.loc[:, 'lesson':]
        self.lesson = lesson_df
        unique_values = next_lesson(self.lesson)[0]
        unique_values.insert(0, 'Select random words from the entire learned vocabulary')
        # close the database connection
        conn2.close()

        # create layout for widget and add list widget
        vbox = QVBoxLayout()
        # create list widget
        self.list_widget = QListWidget()

        # create list item for each unique value in column and add to list widget
        for i, value in enumerate(unique_values):
            if i == 0:
                lesson_text = str(value)
            else:
                lesson_text = 'Lesson ' + str(value)
            self.list_widget.insertItem(i, lesson_text)

        # create a QPushButton widget and add it to the layout
        self.button = QPushButton('Main Menu')
        self.button.clicked.connect(self.main_window_back)

        # connect list item click event to function
        self.list_widget.itemClicked.connect(self.on_lesson_clicked)
        vbox.addWidget(self.list_widget)
        vbox.addWidget(self.button)

        # set layout for widget
        self.setLayout(vbox)

    # function to be performed on item click
    def on_lesson_clicked(self, item):
        if item.text().split(' ')[0] != 'Lesson':
            repeat_lesson = 999
        else:
            repeat_lesson = int(item.text().split(' ')[1])

        conn1 = sqlite3.connect('data_files/words.db')
        df = pd.read_sql('SELECT * FROM words', conn1)
        self.words = df.loc[:, 'word':]
        self.wordList = loadWords(self.words, "yes")
        conn1.close()

        self.lessonNumber = Lesson(repeat_lesson)
        self.lessonNumber.number_of_easy(25)

        if repeat_lesson == 999:
            self.sample = random_sample(all_learned(self.lesson, self.wordList), 25)
        else:
            self.sample = reps(repeat_lesson, self.lesson, self.wordList)


        self.button_grid_window = ButtonGridWidget(repeat=self.sample, lsn=self.lessonNumber, awl=self.wordList)
        self.button_grid_window.move(100, 100)
        self.button_grid_window.show()
        self.button_grid_window.window_closed.connect(self.open_input_counter_widget)
        self.hide()

    def open_input_counter_widget(self):
        self.input_counter_widget = InputCounterWidget(self, self.sample, lsn=self.lessonNumber, awl=self.wordList)
        self.input_counter_widget.move(100, 100)
        self.input_counter_widget.show()

    def main_window_back(self):
        self.close()
        self.main_window.show()


class ButtonGridWidget(QWidget):
    window_closed = pyqtSignal()
    sampleList = pyqtSignal(list)

    def __init__(self, repeat=[], lsn=None, awl=[]):
        super().__init__()

        self.repeat = repeat

        if len(repeat) == 0:
            # connect to the SQLite database and read the data into a pandas dataframe
            # preparation of word list
            conn = sqlite3.connect('data_files/words.db')
            df = pd.read_sql('SELECT * FROM words', conn)
            words = df.loc[:, 'word':]
            wordList = loadWords(words, "yes")
            sample = random_sample(wordList, 25)
            # close the database connection
            conn.close()

            # getting lesson number and creation of lesson object
            conn2 = sqlite3.connect('data_files/lessons.db')
            df = pd.read_sql('SELECT * FROM lessons', conn2)
            # close the database connection
            conn2.close()
            lesson_df = df.loc[:, 'lesson':]
            lessonNumber = Lesson(next_lesson(lesson_df)[1])

        else:
            sample = repeat
            wordList = awl
            # getting lesson number and creation of lesson object
            conn2 = sqlite3.connect('data_files/lessons.db')
            df = pd.read_sql('SELECT * FROM lessons', conn2)
            # close the database connection
            conn2.close()
            lesson_df = df.loc[:, 'lesson':]
            lessonNumber = lsn

        # set the title name for the widget
        self.setWindowTitle(f'Lesson # {lessonNumber.getNumber()}')

        # adding apperance for each word in a sample of words
        [word.addAppear() for word in sample]

        self.shared_object_list = sample
        self.all_word_list = wordList
        self.save = sample.copy()
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

        lessonNumber.wlist([word.getWord() for word in self.save])
        lessonNumber.length_of_lesson(lesson_length(sample))
        lessonNumber.start(datetime.now())
        self.shared_lesson = lessonNumber

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

        if len(self.repeat) == 0:
            self.shared_lesson.number_of_easy(self.counter)

    def closeEvent(self, event):
        self.window_closed.emit()
        self.sampleList.emit([self.shared_object_list, self.shared_lesson, self.all_word_list]) # emit sample of words and lesson object
        super().closeEvent(event)


class ButtonGridWidgetSpare(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, list_of_words=[], rever=0, lsn=999):
        super().__init__()

        self.rever = rever

        if lsn != 999:
            self.lesson = lsn
        else:
            self.lesson = Lesson(1000)

        # set the title name for the widget
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()}')


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

    def __init__(self, main_window, sampleList, awl, nxt=[], rever=0, lsn=999):
        super().__init__()
        if len(nxt) == 0:
            self.list_of_words = sampleList.copy()
        else:
            self.list_of_words = nxt

        if lsn != 999:
            self.lesson = lsn
        else:
            self.lesson = Lesson(1000)

        # set the title name for the widget
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()}')
        self.all_words = awl
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
        self.attempts = 0
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
            self.lesson.points(250 - self.attempts)
            self.lesson.inter(datetime.now())
            self.list_to_delete = []
            self.start_translation()
        elif self.count == 25 and self.rever == 1:
            self.lesson.add_pts(250 - self.attempts)
            self.lesson.finish(datetime.now())
            final_creation_sql(self.all_words, self.lesson)
            self.close()
        elif self.indx == len(self.list_of_words):
            for word in self.list_to_delete:
                self.list_of_words.remove(word)
            self.list_to_delete = []
            self.indx = 0
            random.shuffle(self.list_of_words)
            self.current_word = self.list_of_words[self.indx]
            self.hideMe()
            self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.list_of_words, lsn=self.lesson)
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
            self.current_word.addSuccess()
            if self.rever == 0:
                self.current_word.addTrials_d()
            else:
                self.current_word.addTrials_r()
            self.count += 1
            self.attempts += 1
            self.list_to_delete.append(self.current_word)
            self.indx += 1
            self.lcd_counter.display(self.count)
            self.next_word()
        else:
            if self.rever == 0:
                self.current_word.addTrials_d()
            else:
                self.current_word.addTrials_r()
            self.temp_label.setText(f"{self.current_word.getWord()}, {self.current_word.getTranslation()}") # temporary func
            self.indx += 1
            self.attempts += 1
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
        self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.start_list, lsn=self.lesson)
        self.button_grid_window_spare.move(100, 100)
        self.button_grid_window_spare.window_closed.connect(self.open_tranlsation_counter_widget)
        self.button_grid_window_spare.show()

    def open_tranlsation_counter_widget(self):
        self.input_translation_widget = InputCounterWidget(self, self.start_list, rever=1, lsn=self.lesson, awl=self.all_words)
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

        self.file_menu.addSeparator()

        self.top_ten_action = QAction("TOP 10 lessons", self)
        self.top_ten_action.triggered.connect(self.top_ten)
        self.file_menu.addAction(self.top_ten_action)

        self.bottom_ten_action = QAction("BOTTOM 10 lessons", self)
        self.bottom_ten_action.triggered.connect(self.bottom_ten)
        self.file_menu.addAction(self.bottom_ten_action)

        self.all_lesson_action = QAction("The Worst lessons", self)
        self.all_lesson_action.triggered.connect(self.worst_lessons)
        self.file_menu.addAction(self.all_lesson_action)

        self.file_menu.addSeparator()

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
        pass

    def worst_lessons(self):
        conn2 = sqlite3.connect('data_files/lessons.db')
        df = pd.read_sql('SELECT * FROM lessons', conn2)
        df = df.loc[:, 'lesson':]
        # close the database connection
        conn2.close()
        data = bottom_not_repeated(df)

        # Create and show the text window
        self.text_window = TextWindow(self, data=data)
        self.text_window.move(100, 100)
        self.text_window.show()
        self.hide()

    def top_ten(self):
        data = topbottom()
        # Create and show the text window
        self.text_window = TextWindow(self, data=data)
        self.text_window.move(100, 100)
        self.text_window.show()
        self.hide()

    def bottom_ten(self):
        data = topbottom(top=0)
        # Create and show the text window
        self.text_window = TextWindow(self, data=data)
        self.text_window.move(100, 100)
        self.text_window.show()
        self.hide()

    def next_lesson(self):

        self.button_grid_window = ButtonGridWidget()
        self.button_grid_window.move(100, 100)
        self.button_grid_window.show()
        self.button_grid_window.sampleList.connect(self.open_input_counter_widget)
        self.hide()


    def open_input_counter_widget(self, sampleList):

        sampleList_words = sampleList[0]
        lesson_obj = sampleList[1]
        all_word_list = sampleList[2]

        self.input_counter_widget = InputCounterWidget(self, sampleList=sampleList_words, awl=all_word_list,  lsn=lesson_obj)
        self.input_counter_widget.move(100, 100)
        self.input_counter_widget.show()

    def repeat(self):
        self.repeat_window = RepeatWindow(self)
        self.repeat_window.move(100, 100)
        self.repeat_window.show()
        self.hide()

    def exam(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    main_window = MainWindow()
    main_window.move(100, 100)
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()