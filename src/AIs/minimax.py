from copy import deepcopy
from random import randrange, random

# TODO we should save the listCoeffGain in a file with Amelioration
# and load it with Minimax
class Minimax:
    def __init__(self, game, list_coeff_gain):
        self.game = game
        self.list_coeff_gain = list_coeff_gain

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
            best_move = "END"
            h_gain = float("-inf")
            for move_a in range(6):  # we try every move possible
                gain_move_a = float("inf")
                if self.game.allowed(move_a):
                    b1 = deepcopy(self.game.b)
                    seeds_eaten_a = self.game.move(move_a, board=b1, is_playing=self.game.is_playing)
                    for move_b in range(6):
                        gain_move_a_b = float("inf")
                        if self.game.allowed(move_b, board=b1, is_playing=1 - self.game.is_playing):
                            # move_a and move_b are licit
                            seeds_eaten_b = self.game.move(move_a, board=b1, is_playing=1 - self.game.is_playing)
                            gain_move_a_b = self.gain(b1, self.game.is_playing, seeds_eaten_a, seeds_eaten_b)
                        if gain_move_a_b < gain_move_a:
                            gain_move_a = gain_move_a_b
                if gain_move_a != float("inf"):
                    if gain_move_a > h_gain:
                        h_gain = gain_move_a
                        best_move = move_a
            return best_move

    def gain(self, board, player, seeds_eaten_a, seeds_eaten_b):
        """_this function takes the board we want to evaluate and the
        player for whom we want to evaluate the move."""
        g = self.list_coeff_gain[0] * self.gain_a(seeds_eaten_a) + \
            self.list_coeff_gain[1] * self.gain_a(seeds_eaten_b)
        return g

    def gain_a(self, seeds_eaten_a):
        return seeds_eaten_a

    def gain_b(self, seeds_eaten_b):
        return -seeds_eaten_b
