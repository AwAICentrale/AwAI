import time
from abc import ABC, abstractmethod
from src.AIs.minimax import Minimax
from src.AIs.alea import Alea
from src.AIs.aleaalphabeta import AleaAlphaBeta
from src.AIs.alphabeta import AlphaBeta
from src.AIs.alphabeta import AlphaBetaBegin
from src.AIs.alphabeta import AlphaBetaMidgame
from src.AIs.MCTS import MCTSPlayer

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

    def __init__(self, algo, game, data=None):
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
        elif self.algo == "alphabeta2":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 2, data)  # data is listecoeffgain
        elif self.algo == "alphabeta4":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 4, data)  # data is listecoeffgain
        elif self.algo == "alphabeta6":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 6, data)  # data is listecoeffgain
        elif self.algo == "alphabeta8":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 8, data)  # data is listecoeffgain
        elif self.algo == "alphabeta10":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBeta(self.game, 8, data)  # data is listecoeffgain
        elif self.algo == "alphabetabegin":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBetaBegin(self.game, 2, data)
        elif self.algo == "alphabetamidgame":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]
            self.algo = AlphaBetaMidgame(self.game, 2, data)
        elif self.algo == "mcts":
            self.algo = MCTSPlayer(self.game)

    def play(self):
        return self.algo.play()


class Human(Player):
    """The CLI version of the Human player class that asks the input to the player"""
    def __init__(self, game):
        super().__init__(game)

    def play(self):
        print(self.game.b)

        while 1:
            try:
                pit = int(input("What's your choice (0-5) ? "))
                if not(0 <= pit <= 5):
                    raise ValueError
                else:
                    result = self.game.allowed(pit)
                    if result:
                        return pit
                    else:
                        print("This move is not allowed")
            except ValueError:
                print("You have to enter a value between 0 and 5")

class HumanGUI(Player):
    """The GUI version of the Human player class We need a separate version because of the input. It's very
    unconfortable to link the GUI button to stdin in a polymorphic way. So we use another class and the GUI
    communicates the information through the variable human_player_move """

    def __init__(self, game):
        super().__init__(game)
        self.human_player_move = None

    def play(self):
        while 1:
            self.human_player_move = None
            # we wait 0.2 seconds to not loop 10000 times each seconds without needs
            time.sleep(0.2)
            try:
                if self.human_player_move is None:
                    continue  # No entry yet
                # we check the entry (button press, ie the player wants to move
                pit = int(self.human_player_move) % 6
                # we check the move integrity
                if not (0 <= pit <= 5):
                    raise ValueError
                else:
                    result = self.game.allowed(pit)
                    if result:
                        self.human_player_move = None
                        return pit
                    else:
                        print("This move is not allowed")
            except ValueError:
                print("You have to enter a value between 0 and 5")
