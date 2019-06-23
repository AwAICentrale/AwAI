from copy import deepcopy

class AlphaBeta:
    def __init__(self,game,depth,listCoeffGain):
        self.game = game
        self.listCoeffGain=listCoeffGain
        self.depth = depth

    def play(self):
        eval, move = self.playRec(self.depth, float("-inf"), float("inf"),   \
                    self.game.b, self.game.isPlaying,       \
                    self.game.player1.loft,self.game.player2.loft)
        return move

    def playRec(self, depth, alpha, beta, board, isPlaying, loft1, loft2):
        # we stop the simulation if this part of the simulation give us a winner.
        if (depth == 0) or (loft1 > 24) or (loft2 > 24):
            # We declare attribute that will be used fo the gains
            self.gainBoard = board
            self.gainLoft1 = loft1
            self.gainLoft2 = loft2
            return self.gainMAB(), -1
        
        bestMove = "END"
        
        if isPlaying == self.game.isPlaying:
            maxEval = -float('inf')
            for move in range(6):
                if self.game.allowed(move,board=board):
                    b1 = deepcopy(board)
                    seedsEaten = self.game.move(move, board=b1, isPlaying=isPlaying)
                    if isPlaying == 0:
                        loft1 += seedsEaten
                    else:
                        loft2 += seedsEaten
                    eval, m = self.playRec(depth-1, alpha, beta, b1, 1-isPlaying, loft1, loft2)
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval, bestMove
        
        else:
            minEval = float('inf')
            for move in range(6):
                if self.game.allowed(move,board=board):
                    b1 = deepcopy(board)
                    seedsEaten = self.game.move(move, board=b1, isPlaying=isPlaying)
                    if isPlaying == 0:
                        loft1 += seedsEaten
                    else:
                        loft2 += seedsEaten
                    eval, m = self.playRec(depth-1, alpha, beta, b1, 1-isPlaying, loft1, loft2)
                    if eval < minEval:
                        minEval = eval
                        bestMove = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval, bestMove

    def gainMAB(self):
        a, b, c, d = self.listCoeffGain
        gain = self.gainMAB0() + \
               a*self.gainMAB1() +                      \
               b*self.gainMAB2() +                      \
               c*self.gainMAB3() +                      \
               d*self.gainMAB4()                        
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
        successive = 1      #count the number of 1 or 2 seeds in a row
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
