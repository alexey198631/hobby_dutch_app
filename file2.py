import sys
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
                             QGridLayout, QLabel, QLineEdit, QLCDNumber, QHBoxLayout, QWidgetAction)

from PyQt6.QtGui import QAction


class ButtonGridWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        grid_layout = QGridLayout()

        for i in range(5):
            for j in range(5):
                button = QPushButton(f'Button {i * 5 + j + 1}', self)
                button.setFixedSize(200, 100)
                button.clicked.connect(lambda _, x=i, y=j: self.button_clicked(x, y))
                grid_layout.addWidget(button, i, j)

        self.setLayout(grid_layout)

    def button_clicked(self, x, y):
        print(f"Button at ({x}, {y}) clicked!")
        #self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

class InputCounterWidget(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.label = QLabel("Enter some text:", self)
        self.line_edit = QLineEdit(self)
        self.submit_button = QPushButton("Submit", self)
        self.lcd_counter = QLCDNumber(self)
        self.lcd_counter.setDigitCount(3)
        self.count = 0

        self.submit_button.clicked.connect(self.submit_text)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.line_edit)
        hlayout.addWidget(self.submit_button)
        layout.addLayout(hlayout)

        layout.addWidget(self.lcd_counter)
        self.setLayout(layout)

    def submit_text(self):
        text = self.line_edit.text()
        print(f"Submitted text: {text}")
        self.count += 1
        self.lcd_counter.display(self.count)

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
        print("Show Stat clicked!")


    def next_lesson(self):
        self.button_grid_window = ButtonGridWidget()
        self.button_grid_window.show()
        self.button_grid_window.window_closed.connect(self.open_input_counter_widget)
        self.close()

    def open_input_counter_widget(self):
        self.input_counter_widget = InputCounterWidget()
        self.input_counter_widget.show()
        self.input_counter_widget.window_closed.connect(self.show)
        self.close()

    def repeat(self):
        self.input_counter_widget = InputCounterWidget()
        self.input_counter_widget.show()
        self.input_counter_widget.window_closed.connect(self.show)
        self.close()

    def exam(self):
        self.button_grid_window = ButtonGridWidget()
        self.button_grid_window.show()
        self.button_grid_window.window_closed.connect(self.open_input_counter_widget)
        self.close()

def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeMenuBar)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
