from engine import *

class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""
    def __init__(self,algo1,algo2, nbGame):
        self.game = Game()
        self.game.setPlayers(algo1,algo2)
        self.nbGame = nbGame
        self.stat = [0,0,0]

    def run(self):
        
        for i in range (self.nbGame):
            winner = self.game.runGame()
            if winner == self.game.player1:
                self.stat[0] += 1 
            elif winner == self.game.player2:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
        return self.stat / self.nbGame

    def __repr__(self):
        return "algo {: s} : {: f} % \n \
                algo {: s} : {: f} % \n \
                tied : {: f} % ".format(self.game.player1.algo,self.stat[0],\
                self.game.player2.algo,self.stat[1], self.stat[2])