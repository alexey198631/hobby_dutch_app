import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from random import shuffle

dictionary = {'de': 'the',
 'en': 'and',
 'nog': 'still',
 'maar': 'but'}

class Words(object):

    """The class for all words from dictionary. Each word a type, a translation, an example,
    a translation of an example, a translation to Russian, also additional parameters which would be created after
    the first run (quantity of appearances in lessons, trials of direct and indirect translation,
    success attempts, also weight, more weight - more often words appear"""

    def __init__(self, word, translation):
        self.word = word
        self.translation = translation

    def getWord(self):
        return self.word

    def getTranslation(self):
        return self.translation

list_of_words = []

for d in dictionary.keys():
    list_of_words.append(Words(d, dictionary[d]))


class Quiz(QWidget):
    def __init__(self, list_of_words):
        super().__init__()

        self.questions = list_of_words #list of Class words object
        self.score = 0
        self.attempt = 0
        self.question_index = 0
        self.list_wrong = []

        self.question_label = QLabel()
        self.answer_edit = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.score_label = QLabel()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox.addWidget(self.question_label)
        vbox.addWidget(self.answer_edit)

        hbox.addWidget(self.submit_button)
        hbox.addWidget(self.score_label)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.submit_button.clicked.connect(self.submit_answer)

        self.show_question()

    def show_question(self):
        if self.score == len(self.questions):
            self.question_label.setText("Quiz finished!")
            self.answer_edit.setDisabled(True)
            self.submit_button.setDisabled(True)
            self.score_label.setText(f"Final score: {self.score} / {len(self.questions)}")
        elif self.question_index == len(self.questions) and len(self.list_wrong) > 0:
            self.question_index = self.list_wrong[-1]
            self.list_wrong.pop(self.question_index)
            question = self.questions[self.question_index].getWord()
            self.question_label.setText(question)
            self.answer_edit.setText("")
            self.score_label.setText(f"Score: {self.score} / {len(self.questions)}")
        else:
            question = self.questions[self.question_index].getWord()
            self.question_label.setText(question)
            self.answer_edit.setText("")
            self.score_label.setText(f"Score: {self.score} / {len(self.questions)}")

    def submit_answer(self):
        answer = self.answer_edit.text()
        correct_answer = self.questions[self.question_index].getTranslation()
        if answer == correct_answer:
            self.score += 1
            self.attempt += 1
        else:
            self.attempt += 1
        self.list_wrong.append(self.question_index)
        self.question_index += 1
        self.show_question()


app = QApplication(sys.argv)
window = Quiz(list_of_words)
window.show()
sys.exit(app.exec())