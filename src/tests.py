from src.engine import *


class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""

    def __init__(self, algo0, algo1, nb_game, data0=None, data1=None):
        self.nb_game = nb_game
        self.stat = [0, 0, 0]
        self.algo0 = algo0
        self.algo1 = algo1
        self.data0 = data0
        self.data1 = data1

    def run(self):
        for i in range(self.nb_game):
            game = Game()
            game.set_players(self.algo0, self.algo1, self.data0, self.data1)
            winner = self.game.run_game()
            if winner == self.game.player0:
                self.stat[0] += 1
            elif winner == self.game.player1:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
            print(game.player0.loft, game.player1.loft)
        return [e / self.nb_game for e in self.stat]

    def __repr__(self):
        return f"algo {self.algo0: s} : {self.stat[0]: f} % \n \
                algo {self.algo1: s} : {self.stat[1]: f} % \n \
                tied : {self.stat[2]: f} % "
