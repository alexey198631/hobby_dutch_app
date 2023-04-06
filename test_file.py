from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QGridLayout, QLineEdit, QLabel, QTextEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 400, 300)

        self.button1 = QPushButton("Mode 1", self)
        self.button1.move(50, 50)
        self.button1.clicked.connect(self.open_window1)

        self.button2 = QPushButton("Mode 2", self)
        self.button2.move(50, 100)
        self.button2.clicked.connect(self.open_window2)

        self.button3 = QPushButton("Mode 3", self)
        self.button3.move(50, 150)
        self.button3.clicked.connect(self.open_window3)

        self.inputs = ["input1", "input2", "input3"]
        self.outputs = ["output1", "output2", "output3"]
        self.current_input_index = 0

    def open_window1(self):
        self.window1 = Window1()
        self.window1.show()
        self.hide()

    def open_window2(self):
        self.window2 = Window2()
        self.window2.line_edit.returnPressed.connect(self.process_input)
        self.window2.show()
        self.hide()

    def open_window3(self):
        self.window3 = Window3()
        self.window3.show()
        self.hide()

    def process_input(self):
        input_text = self.window2.line_edit.text()
        output_text = self.outputs[self.current_input_index]
        self.window3.text_edit.append(f"{input_text}: {output_text}")
        self.current_input_index += 1
        if self.current_input_index == len(self.inputs):
            self.current_input_index = 0
            self.window2.close()
            self.open_window3()
        else:
            self.window2.line_edit.setText(self.inputs[self.current_input_index])
            self.window2.label.setText(f"Enter {self.inputs[self.current_input_index]}:")


class Window1(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 1")
        self.setGeometry(100, 100, 400, 300)

        grid_layout = QGridLayout()

        for i in range(25):
            button = QPushButton(f"Button {i+1}", self)
            grid_layout.addWidget(button, i//5, i%5)

        self.setLayout(grid_layout)


class Window2(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 2")
        self.setGeometry(100, 100, 400, 300)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(50, 50)

        self.label = QLabel("Enter your name:", self)
        self.label.move(50, 25)


class Window3(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Window 3")
        self.setGeometry(100, 100, 400, 300)

        self.text_edit = QTextEdit(self)
        self.text_edit.move(50, 50)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
