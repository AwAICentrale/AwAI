from src.player import AI, Human, HumanGUI
from copy import deepcopy
from src.exceptions import StarvationError, EmptyPitError, NotInYourSideError

import argparse
import logging
import time

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", default=0,
                    help="increase verbosity: 0 = only warnings, 1 = info, 2 = debug. Default is no verbosity",
                    action='count')
args = parser.parse_args()
logger = logging.getLogger()
if args.verbose == 0:
    logger.setLevel(logging.WARN)
elif args.verbose == 1:
    logger.setLevel(logging.INFO)
elif args.verbose == 2:
    logger.setLevel(logging.DEBUG)


# TODO add a time clock that provide you the average execution time of one game
class Game:
    def __init__(self, nb_seeds_end=0, GUI=False):
        self.b = Board()
        # _below this number of seeds the game stops
        self.nb_seeds_end = nb_seeds_end
        self.algos_available = ["alea", "alphabeta", "minimax", "aleaalphabeta", "alphabetabegin", "alphabetamidgame",
                                "mcts","fantome"]
        self.is_playing = 0
        self.nb_seeds_eaten = 0
        self.GUI = GUI

    def set_players(self, player0, player1, data0=None, data1=None):
        """you have to call this function to create the type of the players
        before the game starts"""
        if player0 in self.algos_available:
            self.player0 = AI(player0, self, data=data0)
        else:
            if self.GUI:
                self.player0 = HumanGUI(self)
            else:
                self.player0 = Human(self)

        if player1 in self.algos_available:
            self.player1 = AI(player1, self, data=data1)
        else:
            if self.GUI:
                self.player1 = HumanGUI(self)
            else:
                self.player1 = Human(self)

    def run_game(self):
        """the main function that runs the game. _we stop the loop if
        the loft of a player is 24 or more or if the number of seeds on the
        board is below nb_seeds_end."""
        while (self.nb_seeds_eaten < 48 - self.nb_seeds_end) \
                and max(self.player0.loft, self.player1.loft) <= 24 \
                and not (self.nb_seeds_eaten == 46 and self.end_game_is_blocked()):
            # time.sleep(1)
            pit = self.who_is_playing().play()
            rslt_move = self.play(pit)
            if rslt_move == "END":
                self.who_is_playing().add_to_loft(48 - self.nb_seeds_eaten)
                return self.end_of_game()
            # the game stopped, the staying seeds aren't touched
            elif rslt_move == "STOP":
                return self.end_of_game()
            elif rslt_move:
                logging.info("player :" + str(1 - self.is_playing) + " plays : " + str(pit))
                logging.info(f"{self.player0.loft}, {self.player1.loft}")
                logging.info(self.b)
            # print(self.b)

        return self.end_of_game()

    def allowed(self, pit, board=None, is_playing=None):
        """function checking if the move is licit or not
        takes one arguments : number of the pit wanted to be played
        """
        if board is None:
            board = self.b
            logging.debug("REAL MOVE: " + str(pit))
        else:
            logging.debug("SIMULATION : _player " + str(is_playing) + " plays " + str(pit))
        if is_playing is None:
            is_playing = self.is_playing
        try:
            if pit not in range(6):
                raise NotInYourSideError()  # _pit not included in [1,6]

            if board.get_pit(pit + 6 * is_playing) == 0:
                raise EmptyPitError()  # pit wanted is empty

            b1 = deepcopy(board)
            self.move(pit, board=b1, is_playing=is_playing)
            # if opponent's side is not empty
            if not (b1.empty_side(1 - is_playing)):
                return True

            logging.debug("Potentially illicit starving ")
            for move_simulated in range(6):
                # we don't want to change the original board, just to know if it's allowed
                b2 = deepcopy(board)
                #   you must have a seed in the pit you could play
                if board.get_pit(move_simulated + 6 * is_playing) != 0:
                    self.move(move_simulated, board=b2, is_playing=is_playing)
                    # there is a other move that does'nt starve the opponent
                    logging.debug("Try : " + str(move_simulated) + " instead of " + str(pit))
                    logging.debug(b2)
                    if not (b2.empty_side(1 - is_playing)):
                        raise StarvationError()  # so the move is not licit

            # it means the move has to be played but it ends the game
            return "END"
        except NotInYourSideError as e:
            logging.debug(e)
            return False
        except EmptyPitError as e:
            logging.debug(e)
            return False
        except StarvationError as e:
            logging.debug(e)
            return False

    def play(self, pit):
        """function to use in order to play a move on the _board
        it takes one argument : number of the pit wanted to be played"""
        if pit == "END":
            return "END"
        if pit == "STOP":
            return "STOP"
        else:
            self.move(pit)
            return True

    def move(self, pit, board=None, is_playing=None):
        """function moving the seeds on the board and
        it takes one argument : number of the last pit visited
        returns number of seeds captured"""
        if board is None:
            board = self.b
        if is_playing is None:
            is_playing = self.is_playing

        pit += 6 * is_playing
        nb_seeds = board.get_pit(pit)  # saving the number of seeds to sow
        board.set_pit(pit, 0)
        p = pit
        while nb_seeds > 0:
            p = (p + 1) % 12
            if p != pit:  # _we don't put any seeds in the starting pit
                board.add_pit(p, 1)
                nb_seeds -= 1

        # last seeds is indeed in opponent's side and there is 2 or 3 seeds in the pit
        seeds_eaten = 0
        while (6 * (1 - is_playing) <= p <= 5 + 6 * (1 - is_playing)) and (2 <= board.get_pit(p) <= 3):
            seeds_eaten += board.get_pit(p)
            board.set_pit(p, 0)
            p -= 1

        # we only update the loft and the player if it's a play on the real board
        # we shouldn't move the seed on the board if we force the player
        if board == self.b and is_playing == self.is_playing:
            self.who_is_playing().add_to_loft(seeds_eaten)
            self.is_playing = 1 - self.is_playing

        return seeds_eaten

    def who_is_playing(self):
        if self.is_playing == 0:
            return self.player0
        else:
            return self.player1

    def end_of_game(self):
        logging.info(self.b)
        if self.player0.loft > self.player1.loft:  # return nb of the inner
            return self.player0
        elif self.player0.loft < self.player1.loft:
            return self.player1
        else:
            return None

    def end_game_is_blocked(self):
        if self.b.board == [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]:
            self.player0.add_to_loft(1)
            self.player1.add_to_loft(1)
            self.b = [0] * 12
            return True
        return False


class Board:
    def __init__(self):
        self.board = [4 for i in range(12)]

    def __repr__(self):
        s = "  ====================j1=================\n"
        s += "  ||"
        for k in range(11, 5, -1):  # higher part
            if self.board[k] // 10 == 0:
                s += " " + str(self.board[k]) + "  | "
            else:  # if nb_seeds >= 10
                s += " " + str(self.board[k]) + " | "
        s += "|\n"
        s += "  =======================================\n"
        s += "  ||"
        for k in range(6):  # the lower part
            if self.board[k] // 10 == 0:
                s += " " + str(self.board[k]) + "  | "
            else:  # if nb_seeds >= 10
                s += " " + str(self.board[k]) + " | "
        s += "|\n  ====================j0================="
        return s

    def get_pit(self, k):
        return self.board[k]

    def set_pit(self, k, val):
        self.board[k] = val

    def add_pit(self, k, val):
        self.board[k] += val

    def empty_side(self, player):
        """_function looking if the side which first pit is ps is empty
        it takes one argument : ps"""
        for k in range(6 * player, 6 * player + 6):
            if self.get_pit(k) != 0:
                return False
        return True
