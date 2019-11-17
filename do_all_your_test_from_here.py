from src.AIs.genetique import Amelioration
from src.tests import Test
import time
from src.engine import Game

# ----- TEST OF GENETIC ALGO
#a = Amelioration(8, 8, 4).amelioration()
#print(a)
# ---- TEST ON ONE CORE -----
t = Test("alphabeta10", "alphabeta2", 1)
t.run()
print(t.game.player0.loft, t.game.player1.loft)
print(list(t.stat))


# ----- TEST ON ALL CORES -----
# t = Test("alea", "alphabeta", 1000)
# t.run_on_all_cores()
# print(t.game.player0.loft, t.game.player1.loft)
# print(list(t.stat))


# ----- TEST vs HUMAN --------
# game = Game()
# game.set_players("alphabeta", "human")
# game.run_game()
