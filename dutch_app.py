"""

- text size at buttons irregular verbs for spanish as well?
- add more verbs

Graphs

- learn possibiliets PyQT for graphs representation

het and de

- add timing
- add results

"""

import sys
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QTime, QDateTime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QGroupBox, QListWidget, QTableWidget, QTableWidgetItem, QTextEdit, QSizePolicy, QMenu)
from PyQt6.QtGui import QAction, QTextOption, QFont, QIcon, QColor, QBrush, QPalette, QFontMetrics
from functools import partial
from utils.func import *


class DeHetWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.dehetlist = loadData('word', dehet='yes')
        self.points = 0

        self.main_window = main_window

        self.setWindowTitle("De of Het Widget")
        self.setFixedSize(400, 200)

        self.word_label = QLabel("Word", self)
        self.word_label.setFont(QFont("Arial", 16))
        self.debutton = QPushButton("De", self)
        self.hetbutton = QPushButton("Het", self)
        self.translation_label = QLabel("Translation", self)
        self.translation_label.setFont(QFont("Arial", 16))


        button_layout = QHBoxLayout()
        button_layout.addWidget(self.debutton)
        button_layout.addWidget(self.hetbutton)

        #self.debutton.clicked.connect(partial(self.check_article, 'de'))
        self.debutton.clicked.connect(lambda: self.check_article("de", self.debutton))

        #self.hetbutton.clicked.connect(partial(self.check_article, 'het'))
        self.hetbutton.clicked.connect(lambda: self.check_article("het", self.hetbutton))

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.word_label)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.translation_label)
        self.result_label = QLabel("0/0", self)
        self.result_label.setFont(QFont("Arial", 16))
        main_layout.addWidget(self.result_label)
        self.exitbutton = QPushButton("Exit", self)
        main_layout.addWidget(self.exitbutton)

        self.setLayout(main_layout)

        self.exitbutton.clicked.connect(self.close)

        self.indx = 0
        self.next_word()

    def next_word(self):

        if self.indx == len(self.dehetlist):
            print(self.points)
            self.close_me()
        else:
            self.current_word = self.dehetlist[self.indx]
        # Set the word label
        self.word_label.setText(f"De of het?:   {self.current_word[1]} ")
        # Set the translation label
        self.translation_label.setText(f"Translation:   {self.current_word[2]} ")

        self.debutton.setStyleSheet("")  # Reset button color
        self.hetbutton.setStyleSheet("")  # Reset button color



    def check_article(self, expected_article, button):
        if expected_article in self.current_word[0]:
            self.points += 1
            button.setStyleSheet("background-color: green;")
            self.indx += 1
            self.result_label.setText(f"{self.points} / {self.indx} ")
        else:
            self.indx += 1
            button.setStyleSheet("background-color: red;")
            self.result_label.setText(f"{self.points} / {self.indx} ")

        QTimer.singleShot(100, self.next_word)



    def main_window_back(self):
        self.close()
        self.main_window.show()

    def close_me(self):
        self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class TextWidget(QMainWindow):

    def __init__(self, main_window, egs='no'):
        super().__init__()

        self.main_window = main_window
        self.egs = egs
        self.unique_values = loadData('lesson')[0]

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
    window_closed = pyqtSignal()

    def __init__(self, main_window, data=None, after_lesson=0):
        super().__init__()

        self.main_window = main_window
        self.after_lesson = after_lesson

        if self.after_lesson != 0:
            # Set the fixed size of the window
            self.setFixedSize(450, 410)
            self.setWindowTitle(f'{data[2]}')
            self.current_index = data[3]
        else:
            self.setFixedSize(350, 380)
            self.setWindowTitle('results')
            self.current_index = False

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

        if self.after_lesson != 0:
            self.table_widget.setColumnWidth(3, 200)  # Set the width of the second column to 200 pixels

        # Set the column names
        column_names = data[1]
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # If data is provided, populate the table with the data
        if data is not None:
            self.populate_table(data)

        if self.after_lesson == 0:
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


        if self.after_lesson == 0:
            # Populate the table with the data
            for i, row in enumerate(table_data):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(val)  #item = QTableWidgetItem(str(val))
                    if j != 0 and j != 3:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Set the text alignment of the cell to center
                        item.setData(Qt.ItemDataRole.DisplayRole, float(val))  # Set the data type of the cell to float
                    # Check if the current row is the one you want to make bold
                    if self.current_index and i == self.current_index:
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                        brush = QBrush(QColor(230, 230, 230))  # Create a light grey brush
                        item.setBackground(brush)
                    elif self.current_index==0 and i == self.current_index:  # in case of 1st place
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                        brush = QBrush(QColor(230, 230, 230))  # Create a light grey brush
                        item.setBackground(brush)
                    self.table_widget.setItem(i, j, item)
        else:
            # Populate the table with the data
            for i, row in enumerate(table_data):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(val)  # item = QTableWidgetItem(str(val))
                    if j != 0:
                        item.setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter)  # Set the text alignment of the cell to center
                        item.setData(Qt.ItemDataRole.DisplayRole, float(val))  # Set the data type of the cell to float
                    # Check if the current row is the one you want to make bold
                    if self.current_index and i == self.current_index:
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                        brush = QBrush(QColor(230, 230, 230))  # Create a light grey brush
                        item.setBackground(brush)
                    elif self.current_index==0 and i == self.current_index:  # in case of 1st place
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                        brush = QBrush(QColor(230, 230, 230))  # Create a light grey brush
                        item.setBackground(brush)
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

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class TextWindowVerbs(QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self, main_window, data=None):
        super().__init__()

        self.main_window = main_window
        self.setFixedSize(450, 410)
        self.setWindowTitle('Most Difficult Verbs')

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
        self.table_widget.setColumnWidth(3, 200)  # Set the width of the second column to 200 pixels

        # Set the column names
        column_names = data[1]
        self.table_widget.setColumnCount(len(column_names))
        self.table_widget.setHorizontalHeaderLabels(column_names)

        # If data is provided, populate the table with the data
        if data is not None:
            self.populate_table(data)

        submit_button = QPushButton("Close")
        submit_button.clicked.connect(self.close)
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

        for i, row in enumerate(table_data):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))  # item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Set the text alignment of the cell to center
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

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class RepeatWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setGeometry(100, 100, 800, 400)  # x, y, width, height
        self.setWindowTitle('Lessons to repeat')

        try:
            unique_values = loadData('lesson')[0]
            unique_values.insert(0, 'Select random words from the entire learned vocabulary')
        except:
            unique_values = ['Nothing to repeat']

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
        if item.text().split(' ')[0] == 'Nothing':
            self.main_window_back()
            return
        elif item.text().split(' ')[0] != 'Lesson':
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

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


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
            sample = wordList

            try:
                self.lessonNumber = Lesson(loadData('lesson')[1])
                self.lessonNumber.setlevel(Difficulty.difficulty)
            except:
                self.lessonNumber = Lesson(1)
                self.lessonNumber.setlevel(Difficulty.difficulty)

        else:
            sample = repeat
            wordList = awl
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
        self.counter_click = 0  # initialize the counter variable
        grid_layout = QGridLayout()

        for i in range(5):

            for j in range(5):
                wrd = self.shared_object_list[i * 5 + j]
                if wrd.getTyp() is not None:
                    #button = QPushButton(f'{wrd.getTyp()} \n \n {wrd.getWord()}', self)  # \n | \n {sample[i * 5 + j].getTranslation()}
                    button = AutoFontSizeButton(f'{wrd.getTyp()} \n \n {wrd.getWord()}', self)
                else:
                    #button = QPushButton(f'{wrd.getWord()}', self)  # \n | \n {sample[i * 5 + j].getTranslation()}
                    button = AutoFontSizeButton(f'{wrd.getWord()}', self)
                button.setFixedSize(200, 100)
                if wrd.getWeight() != 100.0:
                    button.setStyleSheet("background-color: lightblue")
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
            sender.setStyleSheet(sender.property('original_style')) # Restore the original style for words which were learnt before
            font = sender.property('original_font')
            sender.setFont(font)  # Restore the original font size
            self.counter_click -= 1
        else:
            sender.setProperty('clicked', True)
            sender.setProperty('original_style', sender.styleSheet()) # Store the original style
            text = f'{self.shared_object_list[i * 5 + j].getTranslation()} \n | \n {self.shared_object_list[i * 5 + j].getRussian()}'
            sender.setText(text)
            sender.setStyleSheet("background-color: green")  # change the background color of the clicked button

            # Calculate the optimal font size only if the text doesn't fit within the button's dimensions
            font = sender.font()
            metrics = QFontMetrics(font)
            max_width = sender.width() - 3  # Adjust as needed
            max_height = sender.height() - 3  # Adjust as needed
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()

            if text_width > max_width or text_height > max_height:
                font_size = min((max_width / text_width) * font.pointSize(),
                                (max_height / text_height) * font.pointSize()) + 2 # + 2 because it became too small...
                font.setPointSizeF(font_size)
                sender.setFont(font)  # Set the updated font size

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

    def __init__(self, list_of_words=[], rever=0, lsn=999, pts=0):
        super().__init__()

        self.rever = rever
        self.pts = pts

        if lsn != 999:
            self.lesson = lsn
        else:
            self.lesson = Lesson(1000)

        # set the title name for the widget
        start = (datetime.now() - self.lesson.getStart()).total_seconds()
        self.counter = int(round(start, 0)) + 1
        self.compensator = 0
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{self.pts - self.compensator}]')
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
        self.compensator += 1
        self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{self.pts - self.compensator}]')

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class ButtonGridWidgetVerbs(QWidget):
    window_closed = pyqtSignal()
    sampleList = pyqtSignal(list)

    def __init__(self, main_window):
        super().__init__()

        verbs = loadVerbsData('verb')
        sample = verbs

        self.main_window = main_window

        # set the title name for the widget
        self.counter = 0
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        # adding apperance for each verb in a sample of words
        [verb.addAppear() for verb in sample]

        self.shared_object_list = sample
        #self.all_word_list = wordList
        self.save = sample.copy()
        self.counter_click = 0  # initialize the counter variable
        grid_layout = QGridLayout()

        for i in range(5):
            vrb = self.shared_object_list[i]
            for j in range(5):
                if j == 0:
                    button = QPushButton(f'{vrb.getWord()}', self)
                elif j == 1:
                    button = QPushButton(f'{vrb.getSecond()}', self)
                elif j == 2:
                    button = QPushButton(f'{vrb.getThird()}', self)
                elif j == 3:
                    button = QPushButton(f'{vrb.getTranslation()}', self)
                else:
                    button = QPushButton(f'{vrb.getWeight()}', self)
                button.setFixedSize(200, 100)
                if vrb.getWeight() != 100.0:
                    button.setStyleSheet("background-color: lightblue")
                grid_layout.addWidget(button, i, j)
        # Create a button to go next
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.close)
        next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        next_button.setStyleSheet(Styles.button_style)
        grid_layout.addWidget(next_button, i+1, j)
        self.setLayout(grid_layout)

    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')

    def closeEvent(self, event):
        self.window_closed.emit()
        self.sampleList.emit([self.shared_object_list]) # emit sample of words
        super().closeEvent(event)


class ButtonGridWidgetSpareVerbs(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, list_of_words=[],  startTime=datetime.now()):
        super().__init__()

        self.startTime = startTime
        # set the title name for the widget
        start = (datetime.now() - self.startTime).total_seconds()
        self.counter = int(round(start, 0)) + 1
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        self.sample = list_of_words.copy()
        grid_layout = QGridLayout()


        for i in range(5):
            try:
                vrb = self.sample[i]
                for j in range(5):
                    if j == 0:
                        button = QPushButton(f'{vrb.getWord()}', self)
                    elif j == 1:
                        button = QPushButton(f'{vrb.getSecond()}', self)
                    elif j == 2:
                        button = QPushButton(f'{vrb.getThird()}', self)
                    elif j == 3:
                        button = QPushButton(f'{vrb.getTranslation()}', self)
                    else:
                        button = QPushButton(f'{vrb.getWeight()}', self)
                    button.setFixedSize(200, 100)
                    if vrb.getWeight() != 100.0:
                        button.setStyleSheet("background-color: lightblue")
                    grid_layout.addWidget(button, i, j)

            # here is necessary to keep 25 buttons...
            except:
                pass

                #button = QPushButton()
                #button.setFixedSize(200, 100)
                #grid_layout.addWidget(button, i, j)


        # Create a button to go next
        next_button = QPushButton("Next")
        next_button.setCursor(Qt.CursorShape.PointingHandCursor)
        next_button.setStyleSheet(Styles.button_style)
        next_button.clicked.connect(self.close)
        grid_layout.addWidget(next_button, 5, 4)
        self.setLayout(grid_layout)

    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class InputCounterWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window, sampleList, awl, rever=0, lsn=999):
        super().__init__()

        self.resize(500, 275)
        self.rever = rever
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

        self.count = 0
        self.attempts = 0

        # fine for help with letter
        self.penalty = 0
        self.guess_count = 0

        # set the title name for the widget
        start = (datetime.now() - self.lesson.getStart()).total_seconds()
        self.counter = int(round(start, 0))
        if self.rever == 0:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{2000 - self.counter - self.attempts + self.count - self.penalty}]')
        elif self.rever == 1:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{1725 - self.counter - self.attempts + self.count + self.lesson.getInterPoints() - self.penalty}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        self.all_words = awl
        self.rever = rever
        self.main_window = main_window
        self.start_list = sampleList.copy()
        self.label = QLabel("Enter your translation:", self)
        self.label.setFont(QFont("Arial", 16))
        self.line_edit = QLineEdit(self)
        self.line_edit.setFont(QFont("Arial", 16))
        #self.line_edit.setFont(font)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFont(QFont("Arial", 16))

        self.lcd_counter = QLCDNumber(self)
        self.lcd_counter.setDigitCount(3)
        self.lcd_counter_pts = QLCDNumber(self)
        self.lcd_counter_pts.setDigitCount(3)


        self.indx = 0
        self.list_to_delete = []

        self.submit_button.clicked.connect(self.submit_text)
        self.line_edit.returnPressed.connect(self.submit_button.click)

        # Create QGroupBox for special character buttons
        groupBox = QGroupBox('Special Characters', self)
        hbox = QHBoxLayout(groupBox)



        # Create buttons with special characters
        if GlobalLanguage.file_path == 'utils/spanish/':
            spec_buttons = ['1L', 'á', 'í', 'é', 'ó', 'ñ', 'ú', 'ü']
        else:
            spec_buttons = ['1L', 'ö', 'ü', 'à', 'ë', 'ï', 'é', 'è', 'ê', '’']

        for char in spec_buttons:
            button = QPushButton(char, self)
            if char == '1L':
                button.setFixedSize(35, 21)
                button.setStyleSheet("QPushButton {background-color: lightgreen; border-radius: 5px; padding: 5px;}")
            button.clicked.connect(lambda _, ch=char: self.insertChar(ch))
            button.clicked.connect(self.buttonClicked)
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

    def buttonClicked(self):
        if self.guess_count == 3:
            button = self.sender()  # Get the button that was clicked
            button.setStyleSheet("QPushButton {background-color: red; border-radius: 5px; padding: 5px;}")

    def update_title(self):
        self.counter += 1
        if self.rever == 0:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{2000 - self.counter - self.attempts + self.count - self.penalty}]')
        elif self.rever == 1:
            self.setWindowTitle(f'Lesson # {self.lesson.getNumber()} - [{self.counter}] - [{1725 - self.counter - self.attempts + self.count + self.lesson.getInterPoints() - self.penalty}]')

    def next_word(self):
        if self.count == 25 and self.rever == 0:
            self.rever = 1
            self.lesson.points(250 - self.attempts - self.penalty)
            self.lesson.inter(datetime.now())
            self.list_to_delete = []
            self.start_translation(pts=(2000 - self.counter - self.attempts + self.count - self.penalty))
        elif self.count == 25 and self.rever == 1:
            self.lesson.add_pts(250 - self.attempts - self.penalty)
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
            if self.rever == 0:
                self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.list_of_words, lsn=self.lesson, pts=(2000 - self.counter - self.attempts + self.count - self.penalty))
            elif self.rever == 1:
                self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.list_of_words, lsn=self.lesson, pts=(1725 - self.counter - self.attempts + self.count + self.lesson.getInterPoints() - self.penalty))
            self.button_grid_window_spare.move(100, 100)
            self.button_grid_window_spare.window_closed.connect(self.shoeMe)
            self.button_grid_window_spare.show()
        else:
            self.current_word = self.list_of_words[self.indx]

        # Set the question label
        if self.rever == 0:
            self.label.setText(f"Enter your translation for:   {self.current_word.getWord()} ")
        elif self.rever == 1:
            self.label.setText(f"Enter your translation for:   {self.current_word.getTranslation()} ")

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

    def insertChar(self, ch):

        # Insert character into QLineEdit
        if ch == '1L':
            if self.rever == 0 and self.guess_count != 3:
                cword = self.current_word.getTranslation()[0][0]
                self.line_edit.insert(cword)
                self.penalty += 10
                self.guess_count += 1

            elif self.rever == 1 and self.guess_count != 3:
                tword = self.current_word.getWord()[0][0]
                self.line_edit.insert(tword)
                self.penalty += 10
                self.guess_count += 1
        else:
            self.line_edit.insert(ch)

    def start_translation(self, pts):
        self.close()
        self.button_grid_window_spare = ButtonGridWidgetSpare(list_of_words=self.start_list, lsn=self.lesson, pts=pts)
        self.button_grid_window_spare.move(100, 100)
        self.button_grid_window_spare.window_closed.connect(self.open_tranlsation_counter_widget)
        self.button_grid_window_spare.show()

    def open_tranlsation_counter_widget(self):
        self.input_translation_widget = InputCounterWidget(self, self.start_list, rever=1, lsn=self.lesson, awl=self.all_words)
        self.input_translation_widget.move(100, 100)
        self.input_translation_widget.show()
        self.input_translation_widget.window_closed.connect(self.placing)

    def placing(self):
        data = place()
        # Create and show the text window
        self.text_window = TextWindow(self, data=data, after_lesson=1)
        self.text_window.move(100, 100)
        self.text_window.show()
        self.text_window.window_closed.connect(self.main_window_back)

    def main_window_back(self):
        self.main_window.show()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class InputCounterWidgetVerbs(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window, sampleList, rever=0, startTime=datetime.now()):
        super().__init__()

        self.main_window = main_window
        self.startTime = startTime
        self.resize(500, 275)
        self.list_of_words = sampleList.copy()
        random.shuffle(self.list_of_words)
        self.rever = rever
        # set the title name for the widget
        start = (datetime.now() - self.startTime).total_seconds()
        self.counter = int(round(start, 0))
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        # fine for help with letter
        self.penalty = 0
        self.guess_count = 0
        self.start_list = sampleList.copy()
        self.finish_list = sampleList.copy()
        self.label = QLabel("Enter your translation:", self)
        self.label.setFont(QFont("Arial", 16))
        self.line_edit = QLineEdit(self)
        self.line_edit.setFont(QFont("Arial", 16))
        #self.line_edit.setFont(font)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFont(QFont("Arial", 16))

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
        if GlobalLanguage.file_path == 'utils/spanish/':
            spec_buttons = ['1L', 'á', 'í', 'é', 'ó', 'ñ', 'ú', 'ü']
        else:
            spec_buttons = ['1L', 'ö', 'ü', 'à', 'ë', 'ï', 'é', 'è', 'ê', '’']

        for char in spec_buttons:
            button = QPushButton(char, self)
            if char == '1L':
                button.setFixedSize(35, 21)
                button.setStyleSheet("QPushButton {background-color: lightgreen; border-radius: 5px; padding: 5px;}")
            button.clicked.connect(lambda _, ch=char: self.insertChar(ch))
            button.clicked.connect(self.buttonClicked)
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

    def buttonClicked(self):
        if self.guess_count == 3:
            button = self.sender()  # Get the button that was clicked
            button.setStyleSheet("QPushButton {background-color: red; border-radius: 5px; padding: 5px;}")

    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Learning Verbs - [{self.counter}]')

    def next_word(self):
        if self.count == 5 and self.rever == 0:
            self.rever = 1
            self.list_to_delete = []
            self.start_translation()
            self.close()
        elif self.count == 5 and self.rever == 1:
            self.rever = 2
            self.list_to_delete = []
            self.start_translation_2()
            self.close()
        elif self.count == 5 and self.rever == 2:
            self.rever = 3
            self.list_to_delete = []
            self.start_translation_3()
            self.close()
        elif self.count == 5 and self.rever == 3:
            verbs_sql(self.finish_list)
            self.close()
        elif self.indx == len(self.list_of_words):
            for word in self.list_to_delete:
                self.list_of_words.remove(word)
            self.list_to_delete = []
            self.indx = 0
            random.shuffle(self.list_of_words)
            self.current_word = self.list_of_words[self.indx]
            self.hideMe()
            self.button_grid_window_spare_verbs = ButtonGridWidgetSpareVerbs(list_of_words=self.list_of_words, startTime=self.startTime)
            self.button_grid_window_spare_verbs.move(100, 100)
            self.button_grid_window_spare_verbs.window_closed.connect(self.shoeMe)
            self.button_grid_window_spare_verbs.show()
        else:
            self.current_word = self.list_of_words[self.indx]

        # Set the question label
        if self.rever == 0:
            self.label.setText(f"Enter your translation for:  {self.current_word.getWord()} ")
        elif self.rever == 1:
            self.label.setText(f"Enter your translation for:  {self.current_word.getTranslation()} ")
        elif self.rever == 2:
            self.label.setText(f"Enter the second form for the verb:  {self.current_word.getWord()} ")
        elif self.rever == 3:
            self.label.setText(f"Enter the third form for the verb:  {self.current_word.getWord()} ")

        # Clear the answer line edit and result label
        self.line_edit.clear()

    def submit_text(self):
        text = self.line_edit.text()
        if self.rever == 0:
            translation = self.current_word.getTranslation()
        elif self.rever == 1:
            translation = self.current_word.getWord()
        elif self.rever == 2:
            translation = self.current_word.getSecond()
        elif self.rever == 3:
            translation = self.current_word.getThird()
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

    def closeMe(self):
        self.close()

    def insertChar(self, ch):

        # Insert character into QLineEdit
        if ch == '1L':
            if self.rever == 0 and self.guess_count != 3:
                cword = self.current_word.getTranslation()[0][0]
                self.line_edit.insert(cword)
                self.penalty += 10
                self.guess_count += 1

            elif self.rever == 1 and self.guess_count != 3:
                tword = self.current_word.getWord()[0][0]
                self.line_edit.insert(tword)
                self.penalty += 10
                self.guess_count += 1

            elif self.rever == 2 and self.guess_count != 3:
                tword = self.current_word.getSecond()[0][0]
                self.line_edit.insert(tword)
                self.penalty += 10
                self.guess_count += 1

            elif self.rever == 3 and self.guess_count != 3:
                tword = self.current_word.getThird()[0][0]
                self.line_edit.insert(tword)
                self.penalty += 10
                self.guess_count += 1
        else:
            self.line_edit.insert(ch)

    def start_translation(self):
        self.close()
        self.button_grid_window_spare_verbs_one = ButtonGridWidgetSpareVerbs(list_of_words=self.start_list, startTime=self.startTime)
        self.button_grid_window_spare_verbs_one.move(100, 100)
        #self.button_grid_window_spare_verbs_one.window_closed.connect(lambda: self.open_tranlsation_counter_widget_verb(rever=1))
        self.button_grid_window_spare_verbs_one.window_closed.connect(self.open_tranlsation_counter_widget_verb_one)
        self.button_grid_window_spare_verbs_one.show()

    def open_tranlsation_counter_widget_verb_one(self):
        self.input_translation_widget_verbs = InputCounterWidgetVerbs(self, self.start_list, startTime=self.startTime, rever=1)
        self.input_translation_widget_verbs.move(100, 100)
        self.input_translation_widget_verbs.show()
        #self.input_translation_widget_verbs.window_closed.connect(self.main_window_back)

    def start_translation_2(self):
        self.close()
        self.button_grid_window_spare_verbs_two = ButtonGridWidgetSpareVerbs(list_of_words=self.start_list, startTime=self.startTime)
        self.button_grid_window_spare_verbs_two.move(100, 100)
        #self.button_grid_window_spare_verbs_two.window_closed.connect(lambda: self.open_tranlsation_counter_widget_verb(rever=2))
        self.button_grid_window_spare_verbs_two.window_closed.connect(self.open_tranlsation_counter_widget_verb_two)
        self.button_grid_window_spare_verbs_two.show()

    def open_tranlsation_counter_widget_verb_two(self):
        self.close()
        self.input_translation_widget_verbs = InputCounterWidgetVerbs(self, self.start_list, startTime=self.startTime, rever=2)
        self.input_translation_widget_verbs.move(100, 100)
        self.input_translation_widget_verbs.show()
        #self.input_translation_widget_verbs.window_closed.connect(self.main_window_back)

    def start_translation_3(self):
        self.close()
        self.button_grid_window_spare_verbs_three = ButtonGridWidgetSpareVerbs(list_of_words=self.start_list, startTime=self.startTime)
        self.button_grid_window_spare_verbs_three.move(100, 100)
        #self.button_grid_window_spare_verbs_three.window_closed.connect(lambda: self.open_tranlsation_counter_widget_verb(rever=3))
        self.button_grid_window_spare_verbs_three.window_closed.connect(self.open_tranlsation_counter_widget_verb)
        self.button_grid_window_spare_verbs_three.show()

    def open_tranlsation_counter_widget_verb(self):
        self.close()
        self.input_translation_widget_verbs = InputCounterWidgetVerbs(self, self.start_list, startTime=self.startTime, rever=3)
        self.input_translation_widget_verbs.move(100, 100)
        self.input_translation_widget_verbs.show()
        #if rever == 3:
        self.input_translation_widget_verbs.window_closed.connect(self.verbplacing)

    def verbplacing(self):
        data = hardestVerbs()
        # Create and show the text window
        self.text_window_verbs = TextWindowVerbs(self, data=data)
        self.text_window_verbs.move(100, 100)
        self.text_window_verbs.show()
        #print((datetime.now() - self.startTime).total_seconds())
        #self.text_window_verbs.closed_window.connect(self.main_window_back)

    def main_window_back(self):
        self.main_window.show()

    def main_window_hide(self):
        self.main_window.hide()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


class ExamWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window, sampleList, num):
        super().__init__()

        self.main_window = main_window
        self.resize(500, 275)
        self.start_time = QTime.currentTime()
        self.num = num
        self.list_of_words = sampleList.copy()
        self.total_weight = round(sum([i.getWeight() for i in sampleList]), 2)
        self.total_words = total_exam_words()
        self.counter = 0
        self.setWindowTitle(f'Exam session - [{self.counter}]')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)  # Update title every second

        self.start_list = sampleList.copy()
        self.label = QLabel("Enter your translation:", self)
        self.label.setFont(QFont("Arial", 16))
        self.line_edit = QLineEdit(self)
        self.line_edit.setFont(QFont("Arial", 16))
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setFont(QFont("Arial", 16))

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
        groupBox = QGroupBox('Open the first letter or use Special Characters', self)
        hbox = QHBoxLayout(groupBox)

        # Create buttons with special characters
        # Create buttons with special characters
        if GlobalLanguage.file_path == 'utils/spanish/':
            spec_buttons = ['1L', 'á', 'í', 'é', 'ó', 'ñ', 'ú', 'ü']
        else:
            spec_buttons = ['1L', 'ö', 'ü', 'à', 'ë', 'ï', 'é', 'è', 'ê', '’']
        for char in spec_buttons:
            button = QPushButton(char, self)
            if char == '1L':
                button.setFixedSize(35, 21)
                button.setStyleSheet("QPushButton {background-color: lightgreen; border-radius: 5px; padding: 5px;}")
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

        self.label_answer = QLabel("", self)

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self.lcd_counter)
        hlayout2.addWidget(self.lcd_counter_pts)
        layout.addLayout(hlayout2)
        layout.addWidget(groupBox)
        layout.addWidget(self.label_answer)
        self.setLayout(layout)

        # Start quiz
        self.next_word()

    def update_title(self):
        self.counter += 1
        self.setWindowTitle(f'Exam session - [{self.counter}] - [{self.num - self.attempts}]')

    def next_word(self):
        if self.attempts == self.num:
            current_time = QTime.currentTime()
            elapsed_time = self.start_time.secsTo(current_time)
            self.time_minutes = elapsed_time // 60
            self.time_seconds = elapsed_time % 60
            self.finalresults()
        elif self.indx == len(self.list_of_words):
            for word in self.list_to_delete:
                self.list_of_words.remove(word)
            self.list_to_delete = []
            self.indx = 0
            random.shuffle(self.list_of_words)
            self.current_word = self.list_of_words[self.indx]
        else:
            self.current_word = self.list_of_words[self.indx]

        # Set the question label
        if ExamSettings.exam_direction == 'to_english':
            self.label.setText(f"Enter your translation for:   {self.current_word.getWord()} ")
        else:
            self.label.setText(f"Enter your translation for:   {self.current_word.getTranslation()} ")


        # Clear the answer line edit and result label
        self.line_edit.clear()

    def submit_text(self):

        text = self.line_edit.text()
        if ExamSettings.exam_direction == 'to_english':
            self.translation = self.current_word.getTranslation()
        elif ExamSettings.exam_direction == 'from_english':
            self.translation = self.current_word.getWord()
        self.translation = translation_with_comma(self.translation) # create list of all translations
        if text in self.translation:
            self.count += 1
            self.attempts += 1
            self.list_to_delete.append(self.current_word)
            self.indx += 1
            self.lcd_counter.display(self.count)
            self.lcd_counter_pts.display(self.attempts)
            self.next_word()
        else:
            self.label_answer.setText(f"Right answer: {self.translation[0]} ")
            self.indx += 1
            self.attempts += 1
            self.lcd_counter_pts.display(self.attempts)
            self.next_word()

    def finalresults(self):
        self.close()
        self.main_window.hide()

        if ExamSettings.exam_direction == 'to_english':
            lang = 'nl'
        else:
            lang = 'en'

        with DatabaseConnection('exams.db') as conn:

            cursor = conn.cursor()
            # Execute the query
            cursor.execute(f"SELECT COALESCE(MAX(prcnt), 0) FROM exams WHERE size = {self.num} AND lang = '{lang}'")
            # Fetch the result
            best_result = cursor.fetchone()[0]

        best_result = round(best_result, 0)

        correct_answers, total_questions, time_minutes, time_seconds, best_result = self.count, self.attempts, self.time_minutes, self.time_seconds, best_result

        self.exam_results_window = ExamResultsWidget(self, correct_answers, total_questions, time_minutes, time_seconds, best_result)
        self.exam_results_window.move(100, 100)
        self.exam_results_window.show()
        self.exam_results_window.window_closed.connect(self.main_window_back)
        current_date = QDateTime.currentDateTime().date()
        datetime = QDateTime(current_date, self.start_time)
        formatted_datetime = datetime.toString("yy-MM-dd hh:mm:ss.zzz")
        #prcnt = round((self.count / self.num) * 100, 1)
        exam_sql(formatted_datetime, self.num, self.count, self.total_words, lang, self.total_weight)

    def hideMe(self):
        self.hide()

    def shoeMe(self):
        self.show()

    def insertChar(self, ch):
        # Insert character into QLineEdit
        if ch == '1L':
            if ExamSettings.exam_direction == 'to_english':
                self.line_edit.insert(self.current_word.getTranslation()[0][0])
            else:
                self.line_edit.insert(self.current_word.getWord()[0][0])
        else:
            self.line_edit.insert(ch)

    def main_window_back(self):
        self.main_window.show()

    def closeEvent(self, event):
        self.window_closed.emit()
        self.main_window_back()
        super().closeEvent(event)


class ExamResultsWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, main_window, correct_answers, total_questions, time_minutes, time_seconds, best_result):
        super().__init__()

        self.main_window = main_window
        layout = QVBoxLayout()
        self.setLayout(layout)

        font = QFont("Arial", 16)

        result_label = QLabel(f"Results: {correct_answers}/{total_questions}")
        result_label.setFont(font)
        result_color = QColor("green") if correct_answers > best_result else QColor("red")
        result_label.setStyleSheet(f"color: {result_color.name()};")

        time_label = QLabel(f"Time: {time_minutes:02d}:{time_seconds:02d}")
        time_label.setFont(font)

        best_result = int(best_result)

        best_result_label = QLabel(f"Best Result: {best_result}/{total_questions}")
        best_result_label.setFont(font)

        layout.addWidget(result_label)
        layout.addWidget(time_label)
        layout.addWidget(best_result_label)

        self.setWindowTitle("Exam Results")

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

        self.correct_action = QAction("Correct Words", self)
        self.correct_action.triggered.connect(self.correct)
        self.file_menu.addAction(self.correct_action)

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

        # Difficulty menu and actions
        self.exam_menu = self.menuBar().addMenu("Exam Settings")

        # Create the 'direction' submenu
        self.direction_submenu = QMenu("Direction", self)

        # Create the 'to English' sub-action
        self.to_english_action = QAction("To English", self)
        self.to_english_action.triggered.connect(self.dutch_to_english)
        self.direction_submenu.addAction(self.to_english_action)

        # Create the 'from English' sub-action
        self.from_english_action = QAction("From English", self)
        self.from_english_action.triggered.connect(self.english_to_dutch)
        self.direction_submenu.addAction(self.from_english_action)

        # Add the 'direction' submenu to the 'Exam Settings' menu
        self.exam_menu.addMenu(self.direction_submenu)

        # Create the 'Length' submenu
        self.lenght_submenu = QMenu("Length", self)

        # Create the '25' sub-action
        self.twentyfive = QAction("25", self)
        self.twentyfive.triggered.connect(self.twenty_five)
        self.lenght_submenu.addAction(self.twentyfive)

        # Create the '50' sub-action
        self.fifty = QAction("50", self)
        self.fifty.triggered.connect(self.to_fifty)
        self.lenght_submenu.addAction(self.fifty)

        # Create the '100' sub-action
        self.hundred = QAction("100", self)
        self.hundred.triggered.connect(self.to_hundred)
        self.lenght_submenu.addAction(self.hundred)

        # Add the 'direction' submenu to the 'Exam Settings' menu
        self.exam_menu.addMenu(self.lenght_submenu)

        next_lesson_btn = QPushButton('Next Lesson', self)
        next_lesson_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        next_lesson_btn.setStyleSheet(Styles.button_style)

        repeat_btn = QPushButton('Repeat', self)
        repeat_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        repeat_btn.setStyleSheet(Styles.button_style)

        exam_btn = QPushButton('Exam', self)
        exam_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exam_btn.setStyleSheet(Styles.button_style)

        verb_btn = QPushButton('Verbs', self)
        verb_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        verb_btn.setStyleSheet(Styles.button_style)

        if GlobalLanguage.file_path == 'utils/':
            self.de_het_btn = QPushButton('De of het', self)
            self.de_het_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.de_het_btn.setStyleSheet(Styles.button_style)


        exit_btn = QPushButton('Exit', self)
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setStyleSheet(Styles.button_style)

        next_lesson_btn.clicked.connect(self.next_lesson)
        repeat_btn.clicked.connect(self.repeat)
        exam_btn.clicked.connect(self.exam)
        verb_btn.clicked.connect(self.verbs)
        if GlobalLanguage.file_path == 'utils/':
            self.de_het_btn.clicked.connect(self.dehet)
        exit_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(next_lesson_btn)
        layout.addWidget(repeat_btn)
        layout.addWidget(exam_btn)
        layout.addWidget(verb_btn)
        if GlobalLanguage.file_path == 'utils/':
            layout.addWidget(self.de_het_btn)
        layout.addWidget(exit_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dutch_to_english(self):
        ExamSettings.set_direction('to_english')

    def english_to_dutch(self):
        ExamSettings.set_direction('from_english')

    def twenty_five(self):
        new_length = 25
        ExamSettings.set_length(new_length)

    def to_fifty(self):
        new_length = 50
        ExamSettings.set_length(new_length)

    def to_hundred(self):
        new_length = 100
        ExamSettings.set_length(new_length)

    def reset(self):
        todefault()

    def worst_lessons(self):
        data = bottom_not_repeated()
        #print(data[0], data[1])
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

    def dehet(self):
        self.button_de_het_window = DeHetWidget(self)
        self.button_de_het_window.move(100, 100)
        self.button_de_het_window.show()
        self.hide()
        self.button_de_het_window.window_closed.connect(self.main_window_back)

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
        self.input_counter_widget.window_closed.connect(self.main_window_back)

    def main_window_back(self):
        self.show()

    def repeat(self):
        self.repeat_window = RepeatWindow(self)
        self.repeat_window.move(100, 100)
        self.repeat_window.show()
        self.hide() #here hide
        self.repeat_window.window_closed.connect(self.main_window_back)

    def exam(self):
        new_diff = 'exam'
        Difficulty.set_difficluty(new_diff)
        words = loadData('word', exam='yes')
        # preparation of word list
        wordList = loadWords(words)
        self.exam_window = ExamWidget(self, sampleList=wordList, num=ExamSettings.exam_length)
        self.exam_window.move(100, 100)
        self.exam_window.show()
        new_diff = 'standard'
        Difficulty.set_difficluty(new_diff)
        self.hide()  # here hide

    def verbs(self):
        self.button_grid_window_verbs = ButtonGridWidgetVerbs(self)
        self.button_grid_window_verbs.move(100, 100)
        self.button_grid_window_verbs.show()
        self.button_grid_window_verbs.sampleList.connect(self.open_input_counter_widget_verbs)
        self.hide()

    def open_input_counter_widget_verbs(self, sampleList):
        #raise NotImplementedError('Sorry, this functionality is not implemented yet!')
        sampleList_words = sampleList[0]
        self.input_counter_widget_verbs = InputCounterWidgetVerbs(self, sampleList=sampleList_words)
        self.input_counter_widget_verbs.move(100, 100)
        self.input_counter_widget_verbs.show()
        self.input_counter_widget_verbs.window_closed.connect(self.main_window_back)

    def choose_dutch(self):
        new_value = 'utils/'
        GlobalLanguage.set_value(new_value)
        icon_path = GlobalLanguage.file_path + '/icon.png'
        icon = QIcon(icon_path)
        QApplication.instance().setWindowIcon(icon)
        self.de_het_btn.show()

    def choose_spanish(self):
        new_value = 'utils/spanish/'
        GlobalLanguage.set_value(new_value)
        icon_path = GlobalLanguage.file_path + '/icon.png'
        icon = QIcon(icon_path)
        QApplication.instance().setWindowIcon(icon)
        self.de_het_btn.hide()

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

    def correct(self):
        self.correct_window = SearchWindow(self)
        self.correct_window.move(100, 100)
        self.correct_window.show()
        self.hide()


class SearchWindow(QMainWindow):

    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Database Corrector")
        self.resize(400, 200)

        self.main_window = main_window

        # Add a new variable to store the original word
        self.original_word = None

        # Create widgets
        self.search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        # Create fields and labels
        self.field_names = ['Word', 'Type', 'Translation', 'Russian', 'Difficulty']
        self.fields = []
        self.labels = []

        for field_name in self.field_names:
            label = QLabel(field_name + ":")
            field = QLineEdit()

            self.labels.append(label)
            self.fields.append(field)

        # Create buttons
        self.save_button = QPushButton("Save")
        self.close_button = QPushButton("Close")
        self.result_label = QLabel()

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)

        for label, field in zip(self.labels, self.fields):
            layout.addWidget(label)
            layout.addWidget(field)

        layout.addWidget(self.save_button)
        layout.addWidget(self.close_button)
        layout.addWidget(self.result_label)

        # Create main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Connect button signals
        self.search_button.clicked.connect(self.search)
        self.search_input.returnPressed.connect(self.search_button.click)


        self.save_button.clicked.connect(self.save_changes)
        self.close_button.clicked.connect(self.close)

    def search(self):
        self.result_label.setText('')
        search_term = self.search_input.text()
        if not search_term:
            return

        # Connect to the database
        with DatabaseConnection('words.db') as conn:
            cursor = conn.cursor()

            # Execute the query
            query = f"SELECT word, type, translation, russian, difficulty FROM words WHERE word LIKE ? OR translation LIKE ?"
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))

            # Fetch the result
            result = cursor.fetchone()
            if result is None:
                # No matching record found
                for field in self.fields:
                    field.clear()
                self.original_word = None  # Clear the original word
            else:
                # Update the fields with the fetched values
                for field, value in zip(self.fields, result):
                    field.setText(str(value))
                self.original_word = result[0]  # Store the original word

    def save_changes(self):

        # Check if there is a word to update
        if self.original_word is None:
            return

        # Get the new values from the fields
        new_values = [field.text() for field in self.fields]

        # Check if the fields are empty
        if not all(new_values):
            return

        with DatabaseConnection('words.db') as conn:
            cursor = conn.cursor()

            # Update the values in the database
            query = "UPDATE words SET word=?, type=?, translation=?, russian=?, difficulty=? WHERE word=?"
            values = new_values + [self.original_word]  # Use the original word
            cursor.execute(query, values)

        self.result_label.setText('Saved')

    def closeEvent(self, event):
        self.main_window.show()
        self.save_changes()
        super().closeEvent(event)


class AutoFontSizeButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty('original_font', self.font())  # Initialize original_font property

    def resizeEvent(self, event):
        font = self.font()
        metrics = QFontMetrics(font)
        available_width = self.width()
        available_height = self.height()

        text_width = metrics.horizontalAdvance(self.text())
        text_height = metrics.height()

        while text_width > available_width or text_height > available_height:
            font_size = font.pointSize() - 1
            print(font_size)
            font.setPointSize(font_size)
            metrics = QFontMetrics(font)
            text_width = metrics.horizontalAdvance(self.text())
            text_height = metrics.height()

        self.setFont(font)
        super().resizeEvent(event)


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