from player import *

from copy import deepcopy

class Game:
    def __init__(self, nbSeedsEnd=0):
        self.b = Board()
        self.nbSeedsEnd=nbSeedsEnd # Below this nulber of seeds the game stops
        self.algosAvailable = ["random","alphabeta","minimax"]
        self.isPlaying = 0
        self.nbSeedsEaten = 0

    def setPlayers(self, player1, player2):
        if player1 in self.algosAvailable:
            self.player1 = IA(player1, self)
        else:
            self.player1 = Human(self)
        if player2 in self.algosAvailable:
           self.player2 = IA(player2, self)
        else:
            self.player2 = Human(self)
    
    def runGame(self):
        while self.nbSeedsEaten < 48 - self.nbSeedsEnd and max(self.player2.loft,self.player2.loft)<=24:
            print(self.b)
            pit = self.whoIsPlaying().play()
            rsltMove = self.move(pit)
            if rsltMove =="END":
                self.whoIsPlaying().addToLoft(48-self.nbSeedsEaten)
            
        print(self.b)
        if self.player1.loft > self.player2.loft: #return nb of the inner
            return self.player1
        elif self.player1.loft < self.player2.loft:
            return self.player2
        else:
            return None

    def allowed(self, pit):
        """Function checking if the move is licit or not
        Takes one arguments : number of the pit wanted to be played
        """
        # TODO use exceptions to implement each case

        if (pit not in range(1,7)) or self.b.get(pit-1+6*self.isPlaying)==0: # Pit not included in [1,6] or pit wanted is empty
            return False
        cb = deepcopy(self)
        cb.move(pit)#We play
        if not cb.emptySide(6*(cb.player)): #if opponent's side is not empty
            return True
        else : # we need to know if there are licit moves
            for coupSimule in range(1, 7):
                db = deepcopy(self) #For move we do a copy of the board (we don't want to change the original board)
                if coupSimule != pit: # moves different from pit
                    db.move(coupSimule)
                    if not(db.emptySide(6*db.player)):    #there is a other move that does'nt starve the opponent
                        return False                    #so the move is not licit
                return "END" #It means the move has to be played but it ends the game
        return True

    def play(self, pit):
        """Function to use in order to play a move on the Board
        It takes one argument : number of the pit wanted to be played"""
        rslt=self.allowed(pit)
        if rslt=="END":
            return "END"
        elif rslt == False:
            return None
        else:
            return self.move(pit)

    def emptySide(self,ps):
        """Function looking if the side which first pit is ps is empty
        It takes one argument : ps"""
        for k in range(ps, ps+6):
            if self.b.get(k) != 0:
                return False
        return True


    def move(self,pit):
        """Function moving the seeds on the board and
        It takes one argument : number of the last pit visited
        returns number of seeds captured"""

        pit = pit-1+6 * self.isPlaying
        nbSeeds = self.b.get(pit)       #saving the number of seeds to sow
        self.b.set(pit,0)
        p = pit
        while nbSeeds > 0:
            p = (p + 1) % 12
            if p != pit:           #We don't put any seeds in the starting pit
                self.b.add(p,1)
                nbSeeds-=1
        seedsEaten=0
        while (6*(1-self.isPlaying) <= p <= 5+6*(1-self.isPlaying)) and (2 <= self.b.get(p) <= 3):    # Last seeds is indeed in opponent's side and there is 2 or 3 seeds in the pit
            seedsEaten += self.b.get(p)
            self.b.set(p,0)
            p -= 1
           
        self.whoIsPlaying().addToLoft(seedsEaten)
        self.isPlaying = 1 - self.isPlaying
        return seedsEaten

    def whoIsPlaying(self):
        if self.isPlaying == 0:
            return self.player1
        else:
            return self.player2

class Board:
    def __init__(self):
        self.board = [4 for i in range(12)]

    def __repr__(self):
        s="  =======================================\n"
        s+="  ||"
        for k in range(11, 5, -1):              #la partie haute
            if self.board[k]//10 == 0:
                s+=" " + str(self.board[k])+ "  | "
            else:                               #si le nb de graine est >= 10
                s+=" "+ str(self.board[k])+ " | "
        s+="|\n"
        s+="  =======================================\n"
        s+="  ||"
        for k in range(6):                      #la partie basse
            if self.board[k]//10 == 0:
                s+=" " + str(self.board[k])+ "  | "
            else:                               #si le nb de graine est >= 10
                s+=" "+ str(self.board[k])+ " | "
        s+="|\n  ======================================="
        return s

    def get(self, k):
        return self.board[k]

    def set(self, k, val):
        self.board[k] = val

    def add(self, k, val):
        self.board[k] += val