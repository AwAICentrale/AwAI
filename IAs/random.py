from copy import deepcopy
from random import randint

class Random:
    def __init__(self):
        pass
    def play(self):
        listMove=[]
        for moveA in range(1,7): #we try every move possible
            b=deepcopy(self.board) #Copy of the board in order not to change the original one
            rsltMove = b.play(moveA)
            if rsltMove =="END":
                self.board.grenier[self.board.player]+=(48-sum(self.board.grenier))
                #print("End of the game")
            if rsltMove!=None:
                for moveB in range(1,7):
                    b2=deepcopy(b)
                    if b2.play(moveB)!=None: #Move A and B are licit then we add move A to the list of possible moves
                        listMove.append(moveA)
        if listMove==[]:
            return "Empty"
        return listMove[randint(0,len(listMove)-1)]