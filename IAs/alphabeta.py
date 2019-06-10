from copy import deepcopy

class AlphaBeta:
    def __init__(self,board,listFGain,listCoeffGain):
        self.board = board
        if len(listFGain)!=len(listCoeffGain):
            return None
        self.listFGain=listFGain
        self.listCoeffGain=listCoeffGain

    def play(self, depth, alpha, beta, maximizingPlayer, listCoeffGain):
        if (depth == 0) or (self.board.grenier[0] >= 24) or (self.board.grenier[1] >= 24):
            return self.gainMAB(listCoeffGain), -1
        
        bestMove = -1
        
        if maximizingPlayer:
            maxEval = -float('inf')
            for move in range(1, 7):
                MinimaxCopy = deepcopy(self)
                if MinimaxCopy.board.play(move) not in [None, "END"]:
                    eval, m = MinimaxCopy.minimaxAB(depth-1, alpha, beta, False, listCoeffGain)
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval, bestMove
        
        else:
            minEval = float('inf')
            for move in range(1, 7):
                MinimaxCopy = deepcopy(self)
                if MinimaxCopy.board.play(move) not in [None, "END"]:
                    eval, m = MinimaxCopy.minimaxAB(depth-1, alpha, beta, True, listCoeffGain)
                    if eval < minEval:
                        minEval = eval
                        bestMove = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval, bestMove

    def gainMAB(self, listCoeffGain):
        a, b, c, d = listCoeffGain
        gain = self.gainMAB0() + a*self.gainMAB1() + b*self.gainMAB2() + c*self.gainMAB3() + d*self.gainMAB4()
        return gain
    
    def gainMAB0(self):
        if self.board.grenier[self.board.player] >= 24:
            return float('inf')
        elif self.board.grenier[1-self.board.player] >= 24:
            return -float('inf')
        else:
            return 0
    
    def gainMAB1(self):     #return our wined seeds
        return self.board.grenier[self.board.player]/23     #23 max score
    
    def gainMAB2(self):     #return our loosed seeds
        return self.board.grenier[1-self.board.player]/23   #23 max score
    
    def gainMAB3(self):     #count 1 or 2 seeds
        gain = 0
        successive = 1      #count the number of 1 or 2 seeds in a row
        opponent = 1-self.board.player
        for pit in range(6*self.board.player, 6+6*self.board.player):
            sbp = self.board.board[pit]
            if (sbp == 1) or (sbp == 2):
                gain -= 12*sbp*successive
                successive += 1
            else:
                successive = 1
        for pit in range(6*opponent, 6+6*opponent):
            sbp = self.board.board[pit]
            if (sbp == 1) or (sbp == 2):
                gain += 8*sbp*successive    #opponent play first
                successive += 1
            else:
                successive = 1
        return gain/504     #504 max score {12*[(2*1)+(2*2)+...+(2*6)]}
        
    def gainMAB4(self):     #possible moves
        gain = 0
        opponent = 1-self.board.player
        for pit in range(6*self.board.player, 6+6*self.board.player):
            if self.board.board[pit] > 0:
                gain += 1
        for pit in range(6*opponent, 6+6*opponent):        
            if self.board.board[pit] > 0:
                gain -= 1
        return gain/5   #5 max score {+6 -1}
