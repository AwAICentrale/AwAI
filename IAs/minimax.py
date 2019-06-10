from copy import deepcopy

class Minimax:
    def __init__(self,board,listFGain,listCoeffGain):
        self.board = board
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
            b=deepcopy(self.board) #Copy of the board in order not to change the original one
            if b.play(moveA)not in [None,"END"]:
                for moveB in range(1,7):
                    gainMoveAB=float("inf")
                    b2=deepcopy(b)
                    if b2.play(moveB)not in [None,"END"]: #Move A and B are licit then we calculate the gain
                        gainMoveAB=self.gain(moveA,moveB)
                    if gainMoveAB<gainMoveA:
                        gainMoveA=gainMoveAB
            if gainMoveA!=float("inf"):
                if gainMoveA>hGain:
                    hGain=gainMoveA
                    bestMove=moveA
        return bestMove

    def gainA(self,board,moveA,moveB):
        return board.play(moveA)

    def gainB(self,board,moveA,moveB):
        #print("Move A : ",moveA)
        board.play(moveA)
        return -board.play(moveB)

    def gain(self,moveA,moveB):
        dictGain = {"gainA":self.gainA,"gainB":self.gainB}
        g=0
        for i in range(len(self.listFGain)):
            bCopyGain=deepcopy(self.board) #For each gain we do a copy of the board (we don't want to change the original board during gain calculus)
            g+=self.listCoeffGain[i]*dictGain[self.listFGain[i]](bCopyGain,moveA,moveB)
        return g
    
    
   