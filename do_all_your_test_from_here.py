from src.IAs.genetique import Amelioration
from src.tests import Test

#a = Amelioration(5, 5, 4).amelioration()
#print(a)

#t = Test("alphabeta", "minimax", 1200)
#t.run()

t = Test("alphabeta", "alea", 1200)
t.run_on_all_cores()
print(t.stat)
