from random import randrange


class Alea:
    def __init__(self, game):
        self.game = game

    def play(self):
        list_move = [0, 1, 2, 3, 4, 5]
        while list_move:
            move_test = list_move.pop(randrange(0, len(list_move)))
            result = self.game.allowed(move_test)
            if result:  # it is a valid move
                return move_test
            if result == "END":
                return "END"
        return "END"
