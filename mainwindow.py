# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 420)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_3.addWidget(self.pushButton_start)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setObjectName("listView")
        self.verticalLayout_3.addWidget(self.listView)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_nl = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_nl.setObjectName("pushButton_nl")
        self.horizontalLayout.addWidget(self.pushButton_nl)
        self.pushButton_eng = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_eng.setObjectName("pushButton_eng")
        self.horizontalLayout.addWidget(self.pushButton_eng)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_r = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_r.setObjectName("pushButton_r")
        self.verticalLayout.addWidget(self.pushButton_r)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 24))
        self.menubar.setObjectName("menubar")
        self.menuStats = QtWidgets.QMenu(self.menubar)
        self.menuStats.setObjectName("menuStats")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLesson_stats = QtGui.QAction(MainWindow)
        self.actionLesson_stats.setObjectName("actionLesson_stats")
        self.actionWord_stats = QtGui.QAction(MainWindow)
        self.actionWord_stats.setObjectName("actionWord_stats")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionGo_away = QtGui.QAction(MainWindow)
        self.actionGo_away.setObjectName("actionGo_away")
        self.menuStats.addAction(self.actionLesson_stats)
        self.menuStats.addAction(self.actionWord_stats)
        self.menuStats.addSeparator()
        self.menuStats.addAction(self.actionGo_away)
        self.menubar.addAction(self.menuStats.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dutch words"))
        self.pushButton_start.setText(_translate("MainWindow", "Next Lesson"))
        self.label.setText(_translate("MainWindow", "Exam"))
        self.pushButton_nl.setText(_translate("MainWindow", "nl - > eng"))
        self.pushButton_eng.setText(_translate("MainWindow", "eng - > nl"))
        self.pushButton_r.setText(_translate("MainWindow", "Repeat"))
        self.menuStats.setTitle(_translate("MainWindow", "Stats"))
        self.actionLesson_stats.setText(_translate("MainWindow", "Lesson stats"))
        self.actionWord_stats.setText(_translate("MainWindow", "Word stats"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionGo_away.setText(_translate("MainWindow", "Go away"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
