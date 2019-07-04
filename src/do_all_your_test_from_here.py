from src.IAs.genetique import Amelioration
from src.tests import Test

# a = Amelioration(15, 50, 4).amelioration()
# print(a)

t = Test("minimax", "alea", 30)
t.run()

print(t.stat)
