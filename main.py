import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import  QMainWindow, QApplication, QDialog
from gui import Ui_AwAI
from settings import Ui_Dialog
from awaleClass import *

class Settings(QDialog, Ui_Dialog):
    def __init__(self):
        super(Settings,self).__init__()
        self.setupUi(self)

    def accept(self):
        myapp.b = Board()
        myapp.refresh()
        for id,button in enumerate(myapp.buttons):
            button.clicked.connect(lambda state,i=id : myapp.play(i+1)) # use lambda function to connect because we need an arg

        self.destroy()
    def reject(self):
        self.destroy()

class MyMainWindow(QMainWindow, Ui_AwAI):
    def __init__(self):
        super(MyMainWindow,self).__init__()
        self.setupUi(self)
        self.actionNewGame.triggered.connect(self.new)
        self.buttons=[self.pushButton_1,self.pushButton_2,self.pushButton_3,\
        self.pushButton_4,self.pushButton_5,self.pushButton_6,\
        self.pushButton_7,self.pushButton_8,self.pushButton_9,\
        self.pushButton_10,self.pushButton_11,self.pushButton_12]

    def play(self,pit):
        tmp = self.b.play(pit-6 * self.b.player)
        print(pit,tmp)

        if tmp is not None and tmp != "END":
            self.refresh()

    def refresh(self):
        for button,pit in zip(self.buttons,self.b.board):
            self.setValue(button,pit)

    def setValue(self, button, value):
        button.setText(str(value))

    def new(self):
        dialog = Settings()
        sys.exit(dialog.exec_())

    def closeEvent(self, event):
        """To close main function proper"""
        sys.exit(0)

    def close(self):
        """To close settings"""
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyMainWindow()
    myapp.show()
    sys.exit(app.exec_())
