from src.AIs.genetique import Amelioration
from src.tests import Test
import time
from src.engine import Game

# a = Amelioration(5, 5, 4).amelioration()
# print(a)

# t = Test("alphabeta", "alphabeta", 1)
# t.run()
# time.sleep(0.5)
# t = Test("alea", "alphabeta", 1000)
# t.run_on_all_cores()

# t = Test("alphabetaendgame", "alphabetaendgame", 1)
# t.run()
# print(t.game.player0.loft, t.game.player1.loft)
# print(list(t.stat))

game = Game()
game.set_players("human", "human")
game.run_game()
