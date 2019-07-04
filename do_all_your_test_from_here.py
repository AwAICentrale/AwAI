from src.IAs.genetique import Amelioration
from src.tests import Test

a = Amelioration(5, 5, 4).amelioration()
print(a)

t = Test("alphabeta", "minimax", 30)
t.run()

print(t.stat)
