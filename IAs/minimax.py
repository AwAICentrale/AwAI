from copy import deepcopy
# TODO we should save the listCoeffGain in a file with Amelioration
# and load it with Minimax
class Minimax:
    def __init__(self,game,listCoeffGain):
        self.game = game
        self.listCoeffGain=listCoeffGain

    def play(self):
        bestMove = "END"
        hGain=float("-inf")
        loft1, loft2 = self.game.player1.loft, self.game.player2.loft
        for moveA in range(6): #we try every move possible
            gainMoveA=float("inf")
            if self.game.allowed(moveA):
                b1 = deepcopy(self.game.b)
                seedsEatenA = self.game.move(moveA,board=b1,isPlaying=self.game.isPlaying)
                if self.game.isPlaying == 0:
                        loft1 += seedsEatenA
                else:
                        loft2 += seedsEatenA
                for moveB in range(6):
                    gainMoveAB=float("inf")
                    if self.game.allowed(moveB,board=b1):
                        #Move A and B are licit 
                        seedsEatenB = self.game.move(moveA,board=b1,isPlaying=1-self.game.isPlaying)
                        if self.game.isPlaying == 0:
                            loft1 += seedsEatenB
                        else:
                            loft2 += seedsEatenB
                        self.gainBoard = b1
                        self.gainLoft1 = loft1
                        self.gainLoft2 = loft2
                        gainMoveAB = self.gainMAB()
                    if gainMoveAB<gainMoveA:
                        gainMoveA=gainMoveAB
            if gainMoveA!=float("inf"):
                if gainMoveA>hGain:
                    hGain=gainMoveA
                    bestMove=moveA
        return bestMove

    def gainMAB(self):
        a, b, c, d = self.listCoeffGain
        gain = 0*self.gainMAB0() + \
               1*self.gainMAB1() +                      \
               -1*self.gainMAB2() +                      \
               0*self.gainMAB3() +                      \
               0*self.gainMAB4()                        
        return gain
    
    def gainMAB0(self):
        """This gain updates the value of gainMAB to inf if we won and to -inf
        if we lost"""
        if (self.game.isPlaying == 0 and self.gainLoft1 > 24) or \
           (self.game.isPlaying == 1 and self.gainLoft2 > 24):
            return float('inf')
        elif (self.game.isPlaying == 1 and self.gainLoft1 > 24) or \
             (self.game.isPlaying == 0 and self.gainLoft2 > 24):
            return -float('inf')
        else:
            return 0
    
    def gainMAB1(self):
                   #return our wined seeds
        return (self.gainLoft1*(1-self.game.isPlaying) + self.gainLoft2*self.game.isPlaying) /24
    
    def gainMAB2(self):     #return our loosed seeds
        return (self.gainLoft1*self.game.isPlaying + self.gainLoft2*(1-self.game.isPlaying)) /24
    
    def gainMAB3(self):
        """This gain returns a bad score if you have many pits 
        with 1 or 2 seeds in a row and a great score if the oppoenent has many pits
        with 1 or 2 seeds in a row"""
        GAIN_MAX = 504 #504 max score {12*[(2*1)+(2*2)+...+(2*6)]}
        gain = 0
        successive = 1 #count the number of 1 or 2 seeds in a row
        opponent = 1-self.game.isPlaying
        for pit in range(6*self.game.isPlaying, 6+6*self.game.isPlaying):
            sbp = self.game.b.getPit(pit)
            if (sbp == 1) or (sbp == 2):
                gain -= 12*sbp*successive
                successive += 1
            else:
                successive = 1
        for pit in range(6*opponent, 6+6*opponent):
            sbp = self.game.b.getPit(pit)
            if (sbp == 1) or (sbp == 2):
                gain += 8*sbp*successive    #opponent play first
                successive += 1
            else:
                successive = 1
        return gain/GAIN_MAX
        
    def gainMAB4(self):
        """This gain returns a bad score if you don't have a lot of possible moves"""
        GAIN_MAX = 5
        gain = 0
        opponent = 1-self.game.isPlaying
        for pit in range(6*self.game.isPlaying, 6+6*self.game.isPlaying):
            if self.game.b.getPit(pit) > 0:
                gain += 1
        for pit in range(6*opponent, 6+6*opponent):        
            if self.game.b.getPit(pit) > 0:
                gain -= 1
        return gain/GAIN_MAX   #5 max score {+6 -1}
