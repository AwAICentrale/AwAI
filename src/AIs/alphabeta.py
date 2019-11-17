from copy import deepcopy
from random import randrange, random


class AlphaBeta:
    def __init__(self, game, depth, list_coeff_gain):
        self.game = game
        self.list_coeff_gain = list_coeff_gain
        self.depth = depth
        self.flag = "END"

    def play(self):
        list_move = [0, 1, 2, 3, 4, 5]
        while list_move:
            move = list_move.pop(randrange(0, len(list_move)))
            result = self.game.allowed(move)
            if result:
                break
        if self.game.TEST and random() < 0.05:
            return move

        else:
            evaluation, move = self.play_rec(self.depth, float("-inf"), float("inf"),
                                             self.game.b, self.game.is_playing,
                                             self.game.player0.loft, self.game.player1.loft)
        return move

    def play_rec(self, depth, alpha, beta, board, is_playing, loft0, loft1):
        # we stop the simulation if this part of the simulation give us a winner.
        if (depth == 0) or (loft0 > 24) or (loft1 > 24):
            # _we declare attribute that will be used fo the gains
            self.gain_board = board
            self.gain_loft0 = loft0
            self.gain_loft1 = loft1
            return self.gain(), -1

        best_move = self.flag

        if is_playing == self.game.is_playing:
            max_eval = -float('inf')
            for move in range(6):
                if self.game.allowed(move, board=board, is_playing=is_playing):
                    b1 = deepcopy(board)
                    seeds_eaten = self.game.move(move, board=b1, is_playing=is_playing)
                    if is_playing == 0:
                        loft0 += seeds_eaten
                    else:
                        loft1 += seeds_eaten
                    eval, m = self.play_rec(depth - 1, alpha, beta, b1, 1 - is_playing, loft0, loft1)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move

        else:
            min_eval = float('inf')
            for move in range(6):
                if self.game.allowed(move, board=board, is_playing=is_playing):
                    b1 = deepcopy(board)
                    seeds_eaten = self.game.move(move, board=b1, is_playing=is_playing)
                    if is_playing == 0:
                        loft0 += seeds_eaten
                    else:
                        loft1 += seeds_eaten
                    eval, m = self.play_rec(depth - 1, alpha, beta, b1, 1 - is_playing, loft0, loft1)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def gain(self):
        a, b, c, d = self.list_coeff_gain
        gain = self.gain0() + \
               a * self.gain1() + \
               b * self.gain2() + \
               c * self.gain3() + \
               d * self.gain4()
        return gain

    def gain0(self):
        """_this gain updates the value of gain_m_a_b to inf if we won and to -inf
        if we lost"""
        if (self.game.is_playing == 0 and self.gain_loft0 > 24) or \
                (self.game.is_playing == 1 and self.gain_loft1 > 24):
            return 1000
        elif (self.game.is_playing == 1 and self.gain_loft0 > 24) or \
                (self.game.is_playing == 0 and self.gain_loft1 > 24):
            return -1000
        else:
            return 0

    def gain1(self):
        # return our wined seeds
        return (self.gain_loft0 * (1 - self.game.is_playing) + self.gain_loft1 * self.game.is_playing) / 24

    def gain2(self):  # return our loosed seeds
        return (self.gain_loft0 * self.game.is_playing + self.gain_loft1 * (1 - self.game.is_playing)) / 24

    def gain3(self):
        """_this gain returns a bad score if you have many pits
        with 1 or 2 seeds in a row and a great score if the oppoenent has many pits
        with 1 or 2 seeds in a row"""
        GAIN_MAX = 504  # 504 max score {12*[(2*1)+(2*2)+...+(2*6)]}
        gain = 0
        successive = 1  # count the number of 1 or 2 seeds in a row
        opponent = 1 - self.game.is_playing
        for pit in range(6 * self.game.is_playing, 6 + 6 * self.game.is_playing):
            sbp = self.game.b.get_pit(pit)
            if (sbp == 1) or (sbp == 2):
                gain -= 12 * sbp * successive
                successive += 1
            else:
                successive = 1
        for pit in range(6 * opponent, 6 + 6 * opponent):
            sbp = self.game.b.get_pit(pit)
            if (sbp == 1) or (sbp == 2):
                gain += 8 * sbp * successive  # opponent plays first
                successive += 1
            else:
                successive = 1
        return gain / GAIN_MAX

    def gain4(self):
        """_this gain returns a bad score if you don't have a lot of possible moves"""
        GAIN_MAX = 5
        gain = 0
        opponent = 1 - self.game.is_playing
        for pit in range(6 * self.game.is_playing, 6 + 6 * self.game.is_playing):
            if self.game.b.get_pit(pit) > 0:
                gain += 1
        for pit in range(6 * opponent, 6 + 6 * opponent):
            if self.game.b.get_pit(pit) > 0:
                gain -= 1
        return gain / GAIN_MAX  # 5 max score {+6 -1}


class AlphaBetaBegin(AlphaBeta):
    def __init__(self, game, depth, list_coeff_gain):
        super().__init__(game, depth, list_coeff_gain)
        self.nb_seeds_begin = 5
        self.flag = "STOP"

    def play(self):
        if (self.game.player0.loft >= self.nb_seeds_begin) or \
                (self.game.player1.loft >= self.nb_seeds_begin):
            return "STOP"
        return super().play()


class AlphaBetaMidgame(AlphaBeta):
    def __init__(self, game, depth, list_coeff_gain):
        super().__init__(game, depth, list_coeff_gain)
        self.nb_seeds_midgame = 19
        self.flag = "STOP"

    def play(self):
        # print(self.game.b)
        if (self.game.player0.loft >= self.nb_seeds_midgame) or \
                (self.game.player1.loft >= self.nb_seeds_midgame):
            return "STOP"

        return super().play()

# class AlphaBetaEndgame(AlphaBeta):
#    def __init__(self, game, depth, list_coeff_gain):
#        super().__init(game, depth, list_coeff_gain)
#        self.nb_seeds_endgame = 25
#        
#    def play(self):
#        if (self.game.player0.loft >= self.nb_seeds_midgame) or \
#           (self.game.player1.loft >= self.nb_seeds_midgame):
#            return "END"
#        super().play()
