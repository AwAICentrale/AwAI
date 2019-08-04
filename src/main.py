from PyQt5 import QtWidgets
from PyQt5.QtCore import QRunnable, pyqtSlot, QThreadPool, QTimer
from src.GUI.gui import Ui_AwAI
from src.GUI.settings import Ui_Dialog
import src.GUI.image_rc  # important we shall keep it to get the pictures
from src.engine import *
import sys


class Worker(QRunnable):
    """Worker class that will execute the fn function in a thread"""

    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn

    @pyqtSlot()
    def run(self):
        self.fn()


class Settings(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)
        self.choice_player0 = [self.radioButton, self.radioButton_2, self.radioButton_3]
        self.choice_player1 = [self.radioButton_4, self.radioButton_5, self.radioButton_6]

    def accept(self):
        """the accept function create the game and run the functions that will handle the communication between the
        GUI and the engine. """
        my_app.game = Game(GUI=True)

        for button0, button1 in zip(self.choice_player0, self.choice_player1):
            if button0.isChecked():
                if button1 == "Human":
                    algo0 = "humanGUI"
                else:
                    algo0 = button1.text().lower()
            if button1.isChecked():
                if button1 == "Human":
                    algo1 = "humanGUI"
                else:
                    algo1 = button1.text().lower()
        my_app.game.set_players(algo0, algo1)
        my_app.b = my_app.game.b
        my_app.refresh()
        for j, button in enumerate(my_app.buttons):
            button.clicked.connect(lambda state, i=j: my_app.play(i))
            # use lambda function to connect because we need an arg
        self.done(1)
        my_app.run()

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

        self.thread_pool = QThreadPool()

    def run(self):
        """Create the thread pool and set the refresh function every second """
        w0 = Worker(self.game.run_game)
        self.thread_pool.start(w0)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.refresh)
        self.timer.start()

    def play(self, pit):
        """Update the human player variable to the right value. It is the human player play function to check if the
        move is allowed."""
        print(self.game.who_is_playing())
        self.game.who_is_playing().human_player_move = pit

    def refresh(self):
        for button, pit in zip(self.buttons, self.b.board):
            self.setValue(button, pit)

        self.nbGraines1.display(self.game.player0.loft)
        self.nbGraines2.display(self.game.player1.loft)

    def setValue(self, button, value):
        button.setText(str(value))

    def new(self):
        """Create the Settings window"""
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
    my_app = MyMainWindow()
    my_app.show()
    sys.exit(app.exec_())
