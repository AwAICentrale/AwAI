# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AwAI(object):
    def setupUi(self, AwAI):
        AwAI.setObjectName("AwAI")
        AwAI.resize(1136, 849)
        AwAI.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(AwAI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setStyleSheet("image: url(:/newPrefix/awai.png);")
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 4, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 6)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 4, 2, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_1.setText("")
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout.addWidget(self.pushButton_1, 4, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setEnabled(True)
        self.pushButton_10.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_10.setText("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 2, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 4, 3, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_9.setText("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 2, 3, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 4, 4, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_8.setText("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 2, 4, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_12.setText("")
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout.addWidget(self.pushButton_12, 2, 0, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_11.setText("")
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout.addWidget(self.pushButton_11, 2, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(0, 100))
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 2, 5, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        AwAI.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AwAI)
        self.statusbar.setObjectName("statusbar")
        AwAI.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(AwAI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1136, 25))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        AwAI.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(AwAI)
        self.toolBar.setObjectName("toolBar")
        AwAI.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNewGame = QtWidgets.QAction(AwAI)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionQuit = QtWidgets.QAction(AwAI)
        self.actionQuit.setObjectName("actionQuit")
        self.menuOpen.addAction(self.actionNewGame)
        self.menuOpen.addAction(self.actionQuit)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.label_2.setBuddy(self.label_2)

        self.retranslateUi(AwAI)
        self.actionQuit.triggered.connect(AwAI.close)
        QtCore.QMetaObject.connectSlotsByName(AwAI)

    def retranslateUi(self, AwAI):
        _translate = QtCore.QCoreApplication.translate
        AwAI.setWindowTitle(_translate("AwAI", "AwAI"))
        self.label_2.setText(_translate("AwAI", "<html><head/><body><p align=\"center\"><img src=\":/newPrefix/awai.bmp\"/></p></body></html>"))
        self.label.setText(_translate("AwAI", "<html><head/><body><p align=\"center\">Image à venir</p></body></html>"))
        self.menuOpen.setTitle(_translate("AwAI", "Open"))
        self.toolBar.setWindowTitle(_translate("AwAI", "toolBar"))
        self.actionNewGame.setText(_translate("AwAI", "&New Game"))
        self.actionNewGame.setIconText(_translate("AwAI", "New Game"))
        self.actionNewGame.setShortcut(_translate("AwAI", "Ctrl+N"))
        self.actionQuit.setText(_translate("AwAI", "&Quit"))
        self.actionQuit.setIconText(_translate("AwAI", "Quit"))
        self.actionQuit.setShortcut(_translate("AwAI", "Ctrl+Q"))

import image_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AwAI = QtWidgets.QMainWindow()
    ui = Ui_AwAI()
    ui.setupUi(AwAI)
    AwAI.show()
    sys.exit(app.exec_())

