import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the window title and initial size
        self.setWindowTitle('Lesson App')
        self.setGeometry(100, 100, 300, 200)

        # Create the buttons
        next_lesson_btn = QPushButton('Next Lesson', self)
        repeat_btn = QPushButton('Repeat', self)
        exam_btn = QPushButton('Exam', self)

        # Connect the buttons to their respective slots (functions to be executed)
        next_lesson_btn.clicked.connect(self.next_lesson)
        repeat_btn.clicked.connect(self.repeat)
        exam_btn.clicked.connect(self.exam)

        # Create a layout and add the buttons
        layout = QVBoxLayout()
        layout.addWidget(next_lesson_btn)
        layout.addWidget(repeat_btn)
        layout.addWidget(exam_btn)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def next_lesson(self):
        print("Next Lesson clicked!")

    def repeat(self):
        print("Repeat clicked!")

    def exam(self):
        print("Exam clicked!")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
