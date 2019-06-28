from copy import deepcopy
from random import randrange

class Alea:
    def __init__(self,game):
        self.game = game
    def play(self):
        
        listMove = [0,1,2,3,4,5]
        while listMove != []:
            moveTest = listMove.pop(randrange(0,len(listMove)))
            rslt = self.game.allowed(moveTest)
            if rslt: # it is a valid move
                return moveTest
            if rslt == "END":
                return "END"
        return "END"