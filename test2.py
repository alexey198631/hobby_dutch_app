import sys
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class ExamResultsWidget(QWidget):
    def __init__(self, correct_answers, total_questions, time_minutes, time_seconds, best_result, best_time):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        font = QFont("Arial", 16)

        result_label = QLabel(f"Results: {correct_answers}/{total_questions}")
        result_label.setFont(font)
        result_color = QColor("green") if correct_answers > best_result else QColor("red")
        result_label.setStyleSheet(f"color: {result_color.name()};")

        time_label = QLabel(f"Time: {time_minutes:02d}:{time_seconds:02d}")
        time_label.setFont(font)
        time_color = QColor("green") if time_minutes < best_time else QColor("red")
        time_label.setStyleSheet(f"color: {time_color.name()};")

        best_result_label = QLabel(f"Best Result: {best_result}/{total_questions}")
        best_result_label.setFont(font)

        best_time_label = QLabel(f"Best Time: {best_time:02d}:{time_seconds:02d}")
        best_time_label.setFont(font)

        layout.addWidget(result_label)
        layout.addWidget(time_label)
        layout.addWidget(best_result_label)
        layout.addWidget(best_time_label)

        self.setWindowTitle("Exam Results")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    correct_answers = 15
    total_questions = 20
    time_minutes = 15
    time_seconds = 30

    best_result = 18
    best_time = 14

    widget = ExamResultsWidget(correct_answers, total_questions, time_minutes, time_seconds, best_result, best_time)
    widget.show()

    sys.exit(app.exec())
