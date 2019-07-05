from src.AIs.genetique import Amelioration
from src.tests import Test

a = Amelioration(5, 5, 4).amelioration()
print(a)

#t = Test("alea", "alphabeta", 1, 0, [-1, 1, 0, 0])
#t.run()

#t = Test("alphabetaendgame", "alphabetaendgame", 1)
#t.run()
#print(t.game.player0.loft, t.game.player1.loft)
#print(t.stat)