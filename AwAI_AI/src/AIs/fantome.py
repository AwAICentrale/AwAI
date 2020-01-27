from copy import deepcopy
from src.DataBase.criterion import Criterion

class Fantome:
    def __init__(self, game,depth,value_criteron_imitate):
        self.game=game
        self.depth = depth
        self.myValueCriterionImitate1 = value_criteron_imitate[0]
        self.myValueCriterionImitate2 = value_criteron_imitate[1]
        self.myValueCriterionImitate3 = value_criteron_imitate[2]

    def play(self):
        evaluation, move = self.play_rec(self.depth, float("-inf"), float("inf"),  # depth== 4 or 2
                                         self.game, self.game.is_playing,
                                         self.game.player0.loft, self.game.player1.loft)
        return move

    def play_rec(self, depth, alpha, beta, game, is_playing, loft0, loft1):
        # we stop the simulation if this part of the simulation give us a winner.
        best_move = "END"
        if (depth == 0) or (loft0 > 24) or (loft1 > 24):
            max_eval = -float('inf')
            # _we declare attribute that will be used fo the gains
            self.gain_board = game.b
            self.gain_loft0 = loft0
            self.gain_loft1 = loft1
            criterion_total=0
            for move in range(6):
                if game.allowed(move,game.b,is_playing):
                    myCriterion=Criterion(game, move)
                    criterion1=myCriterion.calculate_criterion_less_grains()
                    criterion2=myCriterion.calculate_criterion_nb_choix()
                    criterion3 = myCriterion.calculate_criterion_moins_cases_voisines_petits()
                    #print([criterion1,criterion2,criterion3])
                    criterion_total = self.gain0() + \
                                      self.myValueCriterionImitate1* criterion1+\
                                      self.myValueCriterionImitate2* criterion2+\
                                      self.myValueCriterionImitate3* criterion3
                    if criterion_total > max_eval:
                        max_eval = criterion_total
                        best_move = move
                    alpha = max(alpha, criterion_total)
                    if beta <= alpha:
                        break
            return max_eval, best_move


        if is_playing == self.game.is_playing:
            max_eval = -float('inf')
            for move in range(6):
                if game.allowed(move, game.b, is_playing):
                    game_copy=deepcopy(game)
                    seeds_eaten = game_copy.move(move)
                    if is_playing == 0:
                        loft0 += seeds_eaten
                    else:
                        loft1 += seeds_eaten
                    eval, m = self.play_rec(depth - 1, alpha, beta, game_copy, 1 - is_playing, loft0, loft1)
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
                if game.allowed(move, game.b, is_playing):
                    game_copy=deepcopy(game)
                    seeds_eaten = game_copy.move(move)
                    if is_playing == 0:
                        loft0 += seeds_eaten
                    else:
                        loft1 += seeds_eaten
                    eval, m = self.play_rec(depth - 1, alpha, beta, game_copy, 1 - is_playing, loft0, loft1)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def gain0(self):
        """_this gain updates the value of gain_m_a_b to inf if we won and to -inf
        if we lost"""
        if (self.game.is_playing == 0 and self.gain_loft0 > 24) or \
                (self.game.is_playing == 1 and self.gain_loft1 > 24):
            return float('inf')
        elif (self.game.is_playing == 1 and self.gain_loft0 > 24) or \
                (self.game.is_playing == 0 and self.gain_loft1 > 24):
            return -float('inf')
        else:
            return 0


'''
    def gain1(self):
        # return our wined seeds
        return (self.gain_loft0 * (1 - self.game.is_playing) + self.gain_loft1 * self.game.is_playing) / 24

    def gain2(self):  # return our loosed seeds
        return (self.gain_loft0 * self.game.is_playing + self.gain_loft1 * (1 - self.game.is_playing)) / 24
'''
