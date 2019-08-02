from src.AIs.genetique import Amelioration
from src.tests import Test
import time

a = Amelioration(5, 5, 4).amelioration()
print(a)
# t = Test("alea", "alphabeta", 100, 0)
# t.run()
# time.sleep(0.5)
# t = Test("alea", "alphabeta", 1000, 0)
# t.run_on_all_cores()

# t = Test("alphabetaendgame", "alphabetaendgame", 1)
# t.run()
# print(t.game.player0.loft, t.game.player1.loft)
# print(list(t.stat))
