from abc import ABC, abstractmethod
from IAs.minimax import Minimax
from IAs.random import Random
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
    def __init__(self, algo, game):
        super(game)
        self.algo = algo
        if self.algo == "random":
            self.algo = Random(self.game)
        elif self.algo == "minimax":
            self.algo = Minimax(None,None,None)
        elif self.algo == "minimaxAB":
            self.algo = AlphaBeta(self.game,None,None)
    
    def play(self):
        return self.algo.play()

class Human(Player):
    def __init__(self, game):
        super(game)

    def play(self):
        
        while 1:
            pit = input("What's your choice (1-6)")
            try:
                if type(pit) != int:
                    raise ValueError
                return pit
            except ValueError:
                print("Entrez une valeur entre 1 et 6")
            
            

    