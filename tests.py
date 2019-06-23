from engine import *

class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""
    def __init__(self,algo0,algo1, nbGame):
        self.nbGame = nbGame
        self.stat = [0,0,0]
        self.algo0 = algo0
        self.algo1 = algo1

    def run(self,toPrint=True):
        for i in range (self.nbGame):
            self.game = Game()
            self.game.setPlayers(self.algo0,self.algo1)
            winner = self.game.runGame(toPrint)
            if winner == self.game.player0:
                self.stat[0] += 1 
            elif winner == self.game.player1:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
            print(t.game.player0.loft, t.game.player1.loft)
        return [e/self.nbGame for e in self.stat]

    def __repr__(self):
        return "algo {: s} : {: f} % \n \
                algo {: s} : {: f} % \n \
                tied : {: f} % ".format(self.game.player0.algo,self.stat[0],\
                self.game.player1.algo,self.stat[1], self.stat[2])
t = Test("alphabeta","random",10)
t.run(toPrint=True)


print(t.stat)