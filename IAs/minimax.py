from copy import deepcopy
# TODO we should save the listCoeffGain in a file with Amelioration
# and load it with Minimax
class Minimax:
    def __init__(self,game,listCoeffGain):
        self.game = game
        self.listCoeffGain=listCoeffGain

    def play(self):
        bestMove="END"
        hGain=float("-inf")
        for moveA in range(6): #we try every move possible
            gainMoveA=float("inf")
            if self.game.allowed(moveA):
                b1 = deepcopy(self.game.b)
                seedsEatenA = self.game.move(moveA,board=b1,isPlaying=self.game.isPlaying)
                for moveB in range(6):
                    gainMoveAB=float("inf")
                    if self.game.allowed(moveB,board=b1,isPlaying=1-self.game.isPlaying):
                        #Move A and B are licit 
                        seedsEatenB = self.game.move(moveA,board=b1,isPlaying=1-self.game.isPlaying)
                        gainMoveAB = self.gain(b1,self.game.isPlaying, seedsEatenA, seedsEatenB)
                    if gainMoveAB<gainMoveA:
                        gainMoveA=gainMoveAB
            if gainMoveA!=float("inf"):
                if gainMoveA>hGain:
                    hGain=gainMoveA
                    bestMove=moveA
        return bestMove

    def gain(self,board,player,seedsEatenA,seedsEatenB):
        """This function takes the board we want to evaluate and the 
        player for whom we want to evaluate the move."""
        g = self.listCoeffGain[0] * self.gainA(seedsEatenA) + \
        self.listCoeffGain[1] * self.gainA(seedsEatenB)
        return g
    
    def gainA(self, seedsEatenA):
        return seedsEatenA

    def gainB(self,seedsEatenB):
        return -seedsEatenB