import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        start_action = QAction('Start', self)
        start_action.triggered.connect(self.start)
        fileMenu.addAction(start_action)

        self.setWindowTitle('PyQt6 GUI')
        self.show()

    def start(self):
        self.table_widget = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        df = pd.read_excel('Words.xlsx')

        self.table_widget.setColumnCount(5)

        if df.shape[0] % 5 == 0:
            row_count = df.shape[0] // 5
        else:
            row_count = df.shape[0] // 5 + 1

        self.table_widget.setRowCount(row_count)

        for i in range(df.shape[0]):
            for j in range(5):
                word = df.iloc[i, 0] if df.shape[1] == 1 else df.iloc[i, j]
                self.table_widget.setItem(i // 5, j, QTableWidgetItem(str(word)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
