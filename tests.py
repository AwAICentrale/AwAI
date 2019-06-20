from engine import *

class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""
    def __init__(self,algo1,algo2, nbGame):
        self.nbGame = nbGame
        self.stat = [0,0,0]
        self.algo1 = algo1
        self.algo2 = algo2

    def run(self,toPrint=True):
        for i in range (self.nbGame):
            self.game = Game()
            self.game.setPlayers(self.algo1,self.algo2)
            winner = self.game.runGame(toPrint)
            if winner == self.game.player1:
                self.stat[0] += 1 
            elif winner == self.game.player2:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
        return [e/self.nbGame for e in self.stat]

    def __repr__(self):
        return "algo {: s} : {: f} % \n \
                algo {: s} : {: f} % \n \
                tied : {: f} % ".format(self.game.player1.algo,self.stat[0],\
                self.game.player2.algo,self.stat[1], self.stat[2])
t = Test("minimax","random",100)
t.run(toPrint=True)
print(t.game.player1.loft, t.game.player2.loft)
print(t.stat)