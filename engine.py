from player import *

from copy import deepcopy
from exceptions import *

import time

class Game:
    def __init__(self, nbSeedsEnd=0):
        self.b = Board()
        # Below this number of seeds the game stops
        self.nbSeedsEnd=nbSeedsEnd 
        self.algosAvailable = ["random","alphabeta","minimax"]
        self.isPlaying = 0
        self.nbSeedsEaten = 0

    def setPlayers(self, player1, player2):
        """You have to call this function to create the type of the players 
        before the game starts"""
        if player1 in self.algosAvailable:
            self.player1 = IA(player1, self)
        else:
            self.player1 = Human(self)
        if player2 in self.algosAvailable:
           self.player2 = IA(player2, self)
        else:
            self.player2 = Human(self)
    
    def runGame(self,toPrint=True):
        """The main function that runs the game. We stop the loop if 
        the loft of a player is 24 or more or if the number of seeds on the
        board is below nbSeedsEnd."""
        while (self.nbSeedsEaten < 48 - self.nbSeedsEnd) and max(self.player1.loft,self.player2.loft)<=24:
            pit = self.whoIsPlaying().play()
            rsltMove = self.play(pit)
            time.sleep(0.01)
            if rsltMove and toPrint:
                print(self.b)
                print(self.player1.loft, self.player2.loft)
            if rsltMove =="END":
                self.whoIsPlaying().addToLoft(48-self.nbSeedsEaten)
                return self.endOfGame()
        return self.endOfGame()

    def allowed(self, pit):
        """Function checking if the move is licit or not
        Takes one arguments : number of the pit wanted to be played
        """
        try:
            if (pit not in range(1,7)):
                raise NotInYourSideError() # Pit not included in [1,6]

            if self.b.getPit(pit-1+6*self.isPlaying)==0:
                raise EmptyPitError() # pit wanted is empty

            b1 = deepcopy(self.b)
            self.move(pit,board=b1)

            #if opponent's side is not empty
            if not b1.emptySide(6*(self.isPlaying)): 
                return True

            for coupSimule in range(1, 7):
                #we don't want to change the original board, just to know if it's allowed
                b2 = deepcopy(b1) 
                self.move(coupSimule, b2)
                #there is a other move that does'nt starve the opponent
                if not(b2.emptySide(6*self.isPlaying)):# TODO change this madness
                    raise StarvationError() #so the move is not licit

            #It means the move has to be played but it ends the game
            return "END" 
        except NotInYourSideError as e:
            print(e)
            return e
        except EmptyPitError as e:
            print(e)
            return e 
        except StarvationError as e:
            print(e)
            return e 

    def play(self, pit):
        """Function to use in order to play a move on the Board
        It takes one argument : number of the pit wanted to be played"""
        if pit is None:
            return self.endOfGame()
        elif type(pit) in [NotInYourSideError, StarvationError, EmptyPitError]:
            return False
        else:
            self.move(pit)
            return True

    def move(self,pit,board=None):
        """Function moving the seeds on the board and
        It takes one argument : number of the last pit visited
        returns number of seeds captured"""
        if board is None:
            board = self.b

        pit += 6 * self.isPlaying
        nbSeeds = board.getPit(pit) #saving the number of seeds to sow
        board.setPit(pit,0)
        p = pit
        while nbSeeds > 0:
            p = (p + 1) % 12
            if p != pit: #We don't put any seeds in the starting pit
                board.addPit(p,1)
                nbSeeds-=1

        # Last seeds is indeed in opponent's side and there is 2 or 3 seeds in the pit
        seedsEaten=0
        while (6*(1-self.isPlaying) <= p <= 5+6*(1-self.isPlaying)) and (2 <= board.getPit(p) <= 3):    
            seedsEaten += board.getPit(p)
            board.setPit(p,0)
            p -= 1

        # we only update the loft and the player if it's a play on the real board
        if board == self.b:   
            self.whoIsPlaying().addToLoft(seedsEaten)
            self.isPlaying = 1 - self.isPlaying

        return seedsEaten

    def whoIsPlaying(self):
        if self.isPlaying == 0:
            return self.player1
        else:
            return self.player2

    def endOfGame(self):
        if self.player1.loft > self.player2.loft: #return nb of the inner
            return self.player1
        elif self.player1.loft < self.player2.loft:
            return self.player2
        else:
            return None

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

    def getPit(self, k):
        return self.board[k]

    def setPit(self, k, val):
        self.board[k] = val

    def addPit(self, k, val):
        self.board[k] += val

    def emptySide(self,ps):
        """Function looking if the side which first pit is ps is empty
        It takes one argument : ps"""
        for k in range(ps, ps+6):
            if self.getPit(k) != 0:
                return False
        return True
