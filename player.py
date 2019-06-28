from abc import ABC, abstractmethod
from IAs.minimax import Minimax
from IAs.alea import Alea
from IAs.alphabeta import AlphaBeta

class Player(ABC):
    """Player is an abstract class which fathers IA and Human"""
    def __init__(self,game):
        self.game = game
        self.loft = 0

    @abstractmethod
    def play(self):
        pass
    
    def addToLoft(self,nb):
        self.game.nbSeedsEaten += nb
        self.loft += nb

class IA(Player):
    """docstring for Player."""
    def __init__(self, algo, game, data):
        super().__init__(game)
        self.algo = algo
        
        if self.algo == "alea":
            self.algo = Alea(self.game)
        elif self.algo == "minimax":
            if data is None:
                data = [1,-1]
            self.algo = Minimax(self.game,data)
        elif self.algo == "alphabeta":
            if data is None:
                data = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]        
            self.algo = AlphaBeta(self.game,2,data) # data is listeCoeffGain
    
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
