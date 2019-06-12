from copy import deepcopy

class Minimax:
    def __init__(self,game,listFGain,listCoeffGain):
        self.game = game
        if len(listFGain)!=len(listCoeffGain):
            return None
        self.listFGain=listFGain
        self.listCoeffGain=listCoeffGain

    def play(self):
        bestMove=0
        hGain=float("-inf")
        lGain = len(self.listFGain)*[0]
        for moveA in range(1,7): #we try every move possible
            gainMoveA=float("inf")
            if self.game.allowed(moveA):
                for moveB in range(1,7):
                    gainMoveAB=float("inf")
                    if self.game.allowed(moveB): #Move A and B are licit 
                        gainMoveAB=self.gain(moveA,moveB)
                    if gainMoveAB<gainMoveA:
                        gainMoveA=gainMoveAB
            if gainMoveA!=float("inf"):
                if gainMoveA>hGain:
                    hGain=gainMoveA
                    bestMove=moveA
        return bestMove

    def gain(self,moveA,moveB):
        dictGain = {"gainA":self.gainA,"gainB":self.gainB}
        g=0
        for e, coeff in zip(self.listFGain,self.listCoeffGain):
            #we don't want to change the original board during gain calculus            
            fakeBoard=deepcopy(self.game.b) 
            g += coeff * dictGain[e](fakeBoard,moveA,moveB)
        return g
    
    def gainA(self,fakeBoard,moveA,moveB):
        return self.game.move(moveA,fakeBoard)

    def gainB(self,fakeBoard,moveA,moveB):
        self.game.move(moveA,fakeBoard)
        return -self.game.move(moveB,fakeBoard)