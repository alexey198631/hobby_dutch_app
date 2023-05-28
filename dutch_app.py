"""
To do:

Печатании уроков было бы неплохо сделать фильтр на сложность
if the lesson in top already - not to put it the last .. is it possible to make it bold?
и непонятно, почему окно не закрывается, а открываается наоборот
if now db?? I need to create the initial start version
exam mode
verbs mode
opening the first letter???
logo for app
graps


"""
import sys
import pandas as pd
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QTime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QGroupBox, QListWidget, QTableWidget, QTableWidgetItem, QTextEdit, QSizePolicy)

from PyQt6.QtGui import QAction, QTextOption, QFont, QIcon
from defs import *
import random
from global_language import GlobalLanguage, Difficulty, Styles
import sqlite3


class TextWidget(QMainWindow):

    def __init__(self, main_window, egs='no'):
        super().__init__()

        self.main_window = main_window
        self.egs = egs

        self.unique_values, self.list_of_lessons = loadData('lesson')

        # Set up the main window layout
        main_layout = QVBoxLayout()

        # Set up the horizontal layout
        h_layout = QHBoxLayout()

        # Create a QTextEdit for the left text section
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        h_layout.addWidget(self.text_edit)

        # Create a QListWidget for the right list section
        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(200)  # Set a fixed width for the list widget
        self.list_widget.itemClicked.connect(self.update_text_edit)
        h_layout.addWidget(self.list_widget)

        for i, value in enumerate(self.unique_values):
            lesson_text = 'Lesson ' + str(value)
            self.list_widget.insertItem(i, lesson_text)

        # Add the QHBoxLayout to the main layout
        main_layout.addLayout(h_layout)

        # Set up the QWidget and set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Create a button to go to Main Menu
        submit_button = QPushButton("Main Menu")
        submit_button.clicked.connect(self.main_window_back)
        main_layout.addWidget(submit_button)

        # Set the window size
        if self.egs == "no":
            self.resize(550, 470)
        else:
            self.resize(1000, 470)

    def update_text_edit(self, item):
        self.text_edit.clear()
        repeat = int(item.text().split(' ')[1])

        self.words = get_lesson_words(repeat)
        self.wordList = loadWords(self.words)

        if self.egs == "no":
            for_print = word_list_to_print(self.wordList)
        else:
            for_print = example_list_to_print(self.wordList)

        self.text_edit.setText('\n'.join(for_print))

    def main_window_back(self):
        self.close()
        self.main_window.show()


class TextWindow(QMainWindow):
    def __init__(self, main_window, data=None, after_lesson=0):
        super().__init__()

        self.main_window = main_window

        if after_lesson != 0:
            # Set the fixed size of the window
            self.setFixedSize(450, 410)
        else:
            self.setFixedSize(350, 380)

        # Create a widget to hold the table and text input field
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Create a table widget and add it to the layout
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Set the column widths
        self.table_widget.setColumnWidth(0, 400)  # Set the width of the first column to 400 pixels
        self.table_widget.setColumnWidth(1, 200)  # Set the width of the second column to 200 pixels
        self.table_widget.setColumnWidth(2, 200)  # Set the width of the second column to 200 pixels

        if after_lesson != 0:
            self.table_widget.setColumnWidth(3, 200)  # Set the width of the second column to 200 pixels

        # Set the column names
        column_names = data[1]
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # If data is provided, populate the table with the data
        if data is not None:
            self.populate_table(data)

        if after_lesson == 0:
            # Create a button to go to Main Menu
            submit_button = QPushButton("Main Menu")
            submit_button.clicked.connect(self.main_window_back)
            layout.addWidget(submit_button)
        else:
            # Create a button close
            submit_button = QPushButton("Close")
            submit_button.clicked.connect(self.close_me)
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
        table_data = data[0]

        # Set the number of rows and columns in the table
        self.table_widget.setRowCount(len(table_data))
        self.table_widget.setColumnCount(len(table_data[0]))

        # Populate the table with the data
        for i, row in enumerate(table_data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(val)  #item = QTableWidgetItem(str(val))
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

    def close_me(self):
        self.close()


class RepeatWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setGeometry(100, 100, 800, 400)  # x, y, width, height
        self.setWindowTitle('Lessons to repeat')

        self.lesson = loadData('lesson')
        unique_values = next_lesson(self.lesson)[0]
        unique_values.insert(0, 'Select random words from the entire learned vocabulary')

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
        self.hide()
        if item.text().split(' ')[0] != 'Lesson':
            repeat_lesson = 999
            self.words = get_lesson_words(repeat_lesson)
            self.wordList = loadWords(self.words)
        else:
            repeat_lesson = int(item.text().split(' ')[1])
            self.words = get_lesson_words(repeat_lesson)
            self.wordList = loadWords(self.words)


        self.lessonNumber = Lesson(repeat_lesson)
        self.lessonNumber.setlevel(repeat_difficulty(self.wordList))
        self.lessonNumber.number_of_easy(25)
        self.sample = self.wordList

        self.button_grid_window = ButtonGridWidget(repeat=self.sample, lsn=self.lessonNumber, awl=self.wordList)
        self.button_grid_window.move(100, 100)
        self.button_grid_window.show()
        self.button_grid_window.window_closed.connect(self.open_input_counter_widget)

    def open_input_counter_widget(self):
        self.input_counter_widget = InputCounterWidget(self, self.sample, lsn=self.lessonNumber, awl=self.wordList)
        self.input_counter_widget.move(100, 100)
        self.input_counter_widget.show()
        self.input_counter_widget.window_closed.connect(self.main_window_back)

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

            words = loadData('word')
            # preparation of word list
            wordList = loadWords(words)

            #sample = random_sample(wordList, 25)
            sample = wordList

            lesson_df = loadData('lesson')
            try:
                self.lessonNumber = Lesson(next_lesson(lesson_df)[1])
                self.lessonNumber.setlevel(Difficulty.difficulty)
            except:
                self.lessonNumber = Lesson(1)
                self.lessonNumber.setlevel(Difficulty.difficulty)

        else:
            sample = repeat
            wordList = awl
            lesson_df = loadData('lesson')
            self.lessonNumber = lsn

        # set the title name for the widget
        self.counter = 0
        self.setWindowTitle(f'Lesson # {self.lessonNumber.getNumber()} - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        # adding apperance for each word in a sample of words
        [word.addAppear() for word in sample]

        self.shared_object_list = sample
        self.all_word_list = wordList
        self.save = sample.copy()
        self.lesson = lesson_df
        self.counter_click = 0  # initialize the counter variable
        grid_layout = QGridLayout()

        for i in range(5):

            for j in range(5):
                wrd = self.shared_object_list[i * 5 + j]
                if wrd.getTyp() is not None:
                    button = QPushButton(f'{wrd.getTyp()} \n \n {wrd.getWord()}', self)  # \n | \n {sample[i * 5 + j].getTranslation()}
                else:
                    button = QPushButton(f'{wrd.getWord()}', self)  # \n | \n {sample[i * 5 + j].getTranslation()}
                button.setFixedSize(200, 100)
                button.clicked.connect(lambda _, i=i, j=j: self.on_button_clicked(i, j))

                grid_layout.addWidget(button, i, j)
        # Create a button to go next
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.close)
        next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        next_button.setStyleSheet(Styles.button_style)
        grid_layout.addWidget(next_button, i+1, j)
        self.setLayout(grid_layout)



        self.lessonNumber.wlist([str(word.getWordIndex()) for word in self.save])
        self.lessonNumber.length_of_lesson(lesson_length(sample))
        self.lessonNumber.start(datetime.now())
        self.shared_lesson = self.lessonNumber

    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Lesson # {self.lessonNumber.getNumber()} - [{self.counter}]')

    def on_button_clicked(self, i, j):
        sender = self.sender()
        if sender.property('clicked'):
            sender.setProperty('clicked', False)
            if self.shared_object_list[i * 5 + j].getTyp() is not None:
                sender.setText(f'{self.shared_object_list[i * 5 + j].getTyp()} \n \n {self.shared_object_list[i * 5 + j].getWord()}')
            else:
                sender.setText(f'{self.shared_object_list[i * 5 + j].getWord()}')
            sender.setStyleSheet("")
            self.counter_click -= 1
        else:
            sender.setProperty('clicked', True)
            sender.setText(
                f'{self.shared_object_list[i * 5 + j].getTranslation()} \n | \n {self.shared_object_list[i * 5 + j].getRussian()}')
            sender.setStyleSheet("background-color: green")  # change the background color of the clicked button
            self.counter_click += 1

        sender.style().unpolish(sender)  # update the button's appearance
        sender.style().polish(sender)  # update the button's appearance

        if len(self.repeat) == 0:
            self.shared_lesson.number_of_easy(self.counter_click)

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
        start = (datetime.now() - self.lesson.getStart()).total_seconds()
        self.counter = int(round(start, 0)) + 1
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second



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
        # Create a button to go next
        next_button = QPushButton("Next")
        next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        next_button.setStyleSheet(Styles.button_style)
        next_button.clicked.connect(self.close)
        grid_layout.addWidget(next_button, 5, 4)
        self.setLayout(grid_layout)





    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}]')

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class InputCounterWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window, sampleList, awl, rever=0, lsn=999):
        super().__init__()

        self.list_of_words = sampleList.copy()
        random.shuffle(self.list_of_words)

        if lsn != 999:
            self.lesson = lsn
        else:
            self.lesson = Lesson(1000)

        # Set the font to bold
        #font = QFont()
        #font.setBold(True)
        #font.setFamily("Arial")
        #font.setPointSize(40)
        #font.setWeight(75)

        # set the title name for the widget
        start = (datetime.now() - self.lesson.getStart()).total_seconds()
        self.counter = int(round(start, 0))
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{2000 - self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        self.all_words = awl
        self.rever = rever
        self.main_window = main_window
        self.start_list = sampleList.copy()
        self.label = QLabel("Enter your translation:", self)
        self.line_edit = QLineEdit(self)
        #self.line_edit.setFont(font)
        self.submit_button = QPushButton("Submit", self)

        self.lcd_counter = QLCDNumber(self)
        self.lcd_counter.setDigitCount(3)
        self.lcd_counter_pts = QLCDNumber(self)
        self.lcd_counter_pts.setDigitCount(3)

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

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.lcd_counter)
        hlayout2.addWidget(self.lcd_counter_pts)
        layout.addLayout(hlayout2)
        layout.addWidget(groupBox)
        self.setLayout(layout)

        # Start quiz
        self.next_word()

    def update_title(self):
        self.counter += 1
        if self.rever == 0:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{2000 - self.counter - self.attempts + self.count}]')
        elif self.rever == 1:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{1725 - self.counter - self.attempts + self.count + self.lesson.getInterPoints()}]')

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
            self.placing()
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
            self.lcd_counter_pts.display(self.attempts)
            self.next_word()
        else:
            if self.rever == 0:
                self.current_word.addTrials_d()
            else:
                self.current_word.addTrials_r()
            self.indx += 1
            self.attempts += 1
            self.lcd_counter_pts.display(self.attempts)
            self.next_word()

    def hideMe(self):
        self.hide()

    def shoeMe(self):
        self.show()

    def placing(self):
        lesson_df = loadData('lesson')
        data = place(lesson_df)
        # Create and show the text window
        self.text_window = TextWindow(self, data=data, after_lesson=1)
        self.text_window.move(400, 100)
        self.text_window.show()

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



        self.file_menu.addSeparator()

        self.top_ten_action = QAction("TOP 10 lessons", self)
        self.top_ten_action.triggered.connect(self.top_ten)
        self.file_menu.addAction(self.top_ten_action)

        self.bottom_ten_action = QAction("BOTTOM 10 lessons", self)
        self.bottom_ten_action.triggered.connect(self.bottom_ten)
        self.file_menu.addAction(self.bottom_ten_action)

        self.worst_lesson_action = QAction("The Worst lessons", self)
        self.worst_lesson_action.triggered.connect(self.worst_lessons)
        self.file_menu.addAction(self.worst_lesson_action)

        self.all_lesson_action = QAction("All lessons", self)
        self.all_lesson_action.triggered.connect(self.all_lessons)
        self.file_menu.addAction(self.all_lesson_action)

        self.all_incl_lesson_action = QAction("Lessons overall", self)
        self.all_incl_lesson_action.triggered.connect(self.all_incl_lessons)
        self.file_menu.addAction(self.all_incl_lesson_action)

        self.file_menu.addSeparator()

        self.print_words_action = QAction("Print Lesson Words", self)
        self.print_words_action.triggered.connect(self.print_lesson_words)
        self.file_menu.addAction(self.print_words_action)

        self.print_examples_action = QAction("Print Examples", self)
        self.print_examples_action.triggered.connect(self.print_examples)
        self.file_menu.addAction(self.print_examples_action)

        self.file_menu.addSeparator()

        self.reset_action = QAction("Reset Progress", self)
        self.reset_action.triggered.connect(self.reset)
        self.file_menu.addAction(self.reset_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        # Language menu and actions
        self.language_menu = self.menuBar().addMenu("Language")

        self.dutch_action = QAction("Dutch", self)
        self.dutch_action.triggered.connect(self.choose_dutch)
        self.language_menu.addAction(self.dutch_action)

        self.spanish_action = QAction("Spanish", self)
        self.spanish_action.triggered.connect(self.choose_spanish)
        self.language_menu.addAction(self.spanish_action)

        # Difficulty menu and actions
        self.diff_menu = self.menuBar().addMenu("Difficulty")

        self.easy_action = QAction("Easy", self)
        self.easy_action.triggered.connect(self.choose_easy)
        self.diff_menu.addAction(self.easy_action)

        self.standard_action = QAction("Standard", self)
        self.standard_action.triggered.connect(self.choose_standard)
        self.diff_menu.addAction(self.standard_action)

        self.hard_action = QAction("Hard", self)
        self.hard_action.triggered.connect(self.choose_hard)
        self.diff_menu.addAction(self.hard_action)

        self.very_hard_action = QAction("Very Hard", self)
        self.very_hard_action.triggered.connect(self.choose_very_hard)
        self.diff_menu.addAction(self.very_hard_action)

        next_lesson_btn = QPushButton('Next Lesson', self)
        next_lesson_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_lesson_btn.setStyleSheet(Styles.button_style)

        repeat_btn = QPushButton('Repeat', self)
        repeat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        repeat_btn.setStyleSheet(Styles.button_style)
        
        exam_btn = QPushButton('Exam', self)
        verb_btn = QPushButton('Verbs', self)

        next_lesson_btn.clicked.connect(self.next_lesson)
        repeat_btn.clicked.connect(self.repeat)
        exam_btn.clicked.connect(self.exam)
        verb_btn.clicked.connect(self.verbs)

        layout = QVBoxLayout()
        layout.addWidget(next_lesson_btn)
        layout.addWidget(repeat_btn)
        layout.addWidget(exam_btn)
        layout.addWidget(verb_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def reset(self):
        todefault()

    def worst_lessons(self):
        data = bottom_not_repeated()
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

    def all_lessons(self):
        data = topbottom(top='all')
        # Create and show the text window
        self.text_window = TextWindow(self, data=data)
        self.text_window.move(100, 100)
        self.text_window.show()
        self.hide()

    def all_incl_lessons(self):
        data = topbottom(top='overall')
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
        self.close() #here hide

    def exam(self):
        pass

    def verbs(self):
        pass

    def choose_dutch(self):
        new_value = 'data_files/'
        GlobalLanguage.set_value(new_value)
        icon_path = GlobalLanguage.file_path + '/icon.png'
        icon = QIcon(icon_path)
        QApplication.instance().setWindowIcon(icon)

    def choose_spanish(self):
        new_value = 'data_files/spanish/'
        GlobalLanguage.set_value(new_value)
        icon_path = GlobalLanguage.file_path + '/icon.png'
        icon = QIcon(icon_path)
        QApplication.instance().setWindowIcon(icon)

    def choose_easy(self):
        new_diff = 'easy'
        Difficulty.set_difficluty(new_diff)

    def choose_standard(self):
        new_diff = 'standard'
        Difficulty.set_difficluty(new_diff)

    def choose_hard(self):
        new_diff = 'hard'
        Difficulty.set_difficluty(new_diff)

    def choose_very_hard(self):
        new_diff = 'very hard'
        Difficulty.set_difficluty(new_diff)
        print(Difficulty.difficulty_distribution)

    def print_lesson_words(self):
        self.text_widget = TextWidget(self)
        self.text_widget.move(100, 100)
        self.text_widget.show()
        self.hide()

    def print_examples(self):
        self.text_widget = TextWidget(self, egs='yes')
        self.text_widget.move(100, 100)
        self.text_widget.show()
        self.hide()



def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    # Setting icon for app
    icon_path = GlobalLanguage.file_path + '/icon.png'
    icon = QIcon(icon_path)
    app.setWindowIcon(icon)

    main_window = MainWindow()
    main_window.move(100, 100)
    main_window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()