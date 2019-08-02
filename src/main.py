from PyQt5 import QtWidgets
from src.GUI.gui import Ui_AwAI
from src.GUI.settings import Ui_Dialog
import src.GUI.image_rc
from src.engine import *
import sys


class Settings(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)

    def accept(self):
        myapp.game = Game()
        myapp.game.set_players("human", "human")
        myapp.b = myapp.game.b
        myapp.refresh()
        for j, button in enumerate(myapp.buttons):
            button.clicked.connect(
                lambda state, i=j: myapp.play(i))  # use lambda function to connect because we need an arg
        self.done(1)

    def reject(self):
        self.done(0)


class MyMainWindow(QtWidgets.QMainWindow, Ui_AwAI):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.buttons = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                        self.pushButton_4, self.pushButton_5, self.pushButton_6,
                        self.pushButton_7, self.pushButton_8, self.pushButton_9,
                        self.pushButton_10, self.pushButton_11, self.pushButton_12]

    def play(self, pit):
        tmp = self.game.play(pit % 6)

        if tmp:
            self.refresh()

    def refresh(self):
        for button, pit in zip(self.buttons, self.b.board):
            self.setValue(button, pit)

    def setValue(self, button, value):
        button.setText(str(value))

    def new(self):
        dialog = Settings()
        dialog.exec_()

    def closeEvent(self, event):
        """To close main function proper"""
        sys.exit(0)

    def close(self):
        """To close settings"""
        self.destroy()
        sys.exit(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyMainWindow()
    myapp.show()
    sys.exit(app.exec_())
