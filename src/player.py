from abc import ABC, abstractmethod
from src.AIs.minimax import Minimax
from src.AIs.alea import Alea
from src.AIs.aleaalphabeta import AleaAlphaBeta
from src.AIs.alphabeta import AlphaBeta
from src.AIs.alphabeta import AlphaBetaBegin
from src.AIs.alphabeta import AlphaBetaMidgame


class Player(ABC):
    """Player is an abstract class which fathers IA and Human"""

    def __init__(self, game):
        self.game = game
        self.loft = 0

    @abstractmethod
    def play(self):
        pass

    def add_to_loft(self, nb):
        self.game.nb_seeds_eaten += nb
        self.loft += nb


class AI(Player):
    """docstring for player."""

    def __init__(self, algo, game, data):
        super().__init__(game)
        self.algo = algo

        if self.algo == "alea":
            self.algo = Alea(self.game)
        elif self.algo == "aleaalphabeta":
            if data is None:
                data = "begin"
            self.algo = AleaAlphaBeta(self.game, data)
        elif self.algo == "minimax":
            if data is None:
                data = [1, -1]
            self.algo = Minimax(self.game, data)
        elif self.algo == "alphabeta":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 2, data)  # data is listecoeffgain
        elif self.algo == "alphabetabegin":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBetaBegin(self.game, 2, data)
        elif self.algo == "alphabetamidgame":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBetaMidgame(self.game, 2, data)

    def play(self):
        return self.algo.play()


class Human(Player):
    def __init__(self, game):
        super().__init__(game)

    def play(self):

        while 1:
            pit = input("What's your choice (1-6) ?")
            try:
                if type(pit) != int:
                    raise ValueError
                return pit
            except ValueError:
                print("Enter a value between 1 and 6 :")
