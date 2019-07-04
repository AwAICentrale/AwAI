from src.engine import *


class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""

    def __init__(self, algo0, algo1, nbGame, data0=None, data1=None):
        self.nbGame = nbGame
        self.stat = [0, 0, 0]
        self.algo0 = algo0
        self.algo1 = algo1
        self.data0 = data0
        self.data1 = data1

    # TODO refactor self.game (absurd)
    def run(self):
        for i in range(self.nbGame):
            self.game = Game()
            self.game.setPlayers(self.algo0, self.algo1, self.data0, self.data1)
            winner = self.game.runGame()
            if winner == self.game.player0:
                self.stat[0] += 1
            elif winner == self.game.player1:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
            print(self.game.player0.loft, self.game.player1.loft)
        return [e / self.nbGame for e in self.stat]

    def __repr__(self):
        return f"algo {self.game.player0.algo: s} : {self.stat[0]: f} % \n \
                algo {self.game.player1.algo: s} : {self.stat[1]: f} % \n \
                tied : {self.stat[2]: f} % "
