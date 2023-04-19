import sys
from random import shuffle
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget

class Word:
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.words = [
            Word("apple", "manzana"),
            Word("banana", "plátano"),
            Word("grape", "uva"),
            Word("orange", "naranja"),
            Word("pear", "pera")
        ]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Quiz App")

        main_layout = QVBoxLayout()

        self.label = QLabel("Translate the following words:")
        main_layout.addWidget(self.label)

        self.word_labels = []
        for word in self.words:
            word_label = QLabel(f"{word.word} - {word.translation}")
            main_layout.addWidget(word_label)
            self.word_labels.append(word_label)

        self.start_button = QPushButton("Start Quiz")
        self.start_button.clicked.connect(self.start_quiz)
        main_layout.addWidget(self.start_button)

        self.answer_input = QLineEdit()
        main_layout.addWidget(self.answer_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.check_answer)
        main_layout.addWidget(self.submit_button)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_quiz(self):
        shuffle(self.words)
        self.current_word_index = 0
        self.update_word()

    def update_word(self):
        for label in self.word_labels:
            label.hide()
        self.word_labels[self.current_word_index].show()

    def check_answer(self):
        user_answer = self.answer_input.text().strip()
        correct_answer = self.words[self.current_word_index].translation

        if user_answer.lower() == correct_answer.lower():
            self.current_word_index += 1
            if self.current_word_index < len(self.words):
                self.update_word()
            else:
                self.label.setText("Congratulations! You won!")
                self.answer_input.clear()
        else:
            self.label.setText(f"Incorrect! Try again.")
            self.answer_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QuizApp()
    main_window.show()
    sys.exit(app.exec())
