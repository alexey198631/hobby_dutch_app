import sys
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import *

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Learn Dutch Words and Play")
window.setFixedWidth(1280)
window.setFixedHeight(720)
window.move(0, 0)
window.setStyleSheet("background: #DAA520;")

grid = QGridLayout()

# display logo
image = QPixmap('dutch.png')
logo = QLabel()
logo.setPixmap(image)
logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
logo.setStyleSheet("margin-top: 100px;")

# button widget
button = QPushButton("PLAY")
button.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
button.setStyleSheet(
    "*{border: 4px solid '#BC006C';" +
    "border-radius: 45px;" +
    "font-size: 35 px;" +
    "color: 'White';" +
    "padding: 25px 0;" +
    "margin: 10px 20px}" +
    "*:hover{background: '#BC006C';}"
)


grid.addWidget(logo, 0, 0)
grid.addWidget(button, 1, 0)


window.setLayout(grid)

window.show()
sys.exit(app.exec())