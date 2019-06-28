from player import *

from copy import deepcopy
from exceptions import *

import sys
import time

# TODO add a time clock that provide you the average execution time of one game
class Game:
    def __init__(self, nbSeedsEnd=0):
        self.b = Board()
        # Below this number of seeds the game stops
        self.nbSeedsEnd=nbSeedsEnd 
        self.algosAvailable = ["alea","alphabeta","minimax"]
        self.isPlaying = 0
        self.nbSeedsEaten = 0

    def setPlayers(self, player0, player1,data0=None, data1=None):
        """You have to call this function to create the type of the players 
        before the game starts"""
        if player0 in self.algosAvailable:
            self.player0 = IA(player0, self, data=data0)
        else:
            self.player0 = Human(self)
        if player1 in self.algosAvailable:
           self.player1 = IA(player1, self, data=data1)
        else:
            self.player1 = Human(self)
    
    def runGame(self,toPrint=True):
        """The main function that runs the game. We stop the loop if 
        the loft of a player is 24 or more or if the number of seeds on the
        board is below nbSeedsEnd."""
        while (self.nbSeedsEaten < 48 - self.nbSeedsEnd) \
        and max(self.player0.loft,self.player1.loft)<=24 \
        and not(self.nbSeedsEaten == 46 and self.endGameIsBlocked()):
            #time.sleep(0.01)
            pit = self.whoIsPlaying().play()
            rsltMove = self.play(pit)
            if rsltMove == "END":
                self.whoIsPlaying().addToLoft(48-self.nbSeedsEaten)
                return self.endOfGame()

            elif rsltMove and toPrint:
                print("Player :" + str(1-self.isPlaying) + " plays : " + str(pit))
                print(self.player0.loft, self.player1.loft)
                print(self.b)
            
        return self.endOfGame()

    def allowed(self, pit, board=None, isPlaying=None):
        """Function checking if the move is licit or not
        Takes one arguments : number of the pit wanted to be played
        """
        if board is None:
            board = self.b
            print("REAL MOVE : " + str(pit))
        else:
            print("SIMULATION : Player " + str(isPlaying) + " plays " + str(pit))
        if isPlaying is None:
            isPlaying = self.isPlaying
        try:
            if (pit not in range(6)):
                raise NotInYourSideError() # Pit not included in [1,6]

            if board.getPit(pit+6*isPlaying)==0:
                raise EmptyPitError() # pit wanted is empty

            b1 = deepcopy(board)
            self.move(pit,board=b1,isPlaying=isPlaying)
            #if opponent's side is not empty
            if not(b1.emptySide(1 - isPlaying)): 
                return True

            
            print("potentially illicit starving ")
            for coupSimule in range(6):
                #we don't want to change the original board, just to know if it's allowed
                b2 = deepcopy(board)
                #YOU MUST HAVE A SEED IN THE PIT YOU COULD PLAY
                if board.getPit(coupSimule + 6*isPlaying) != 0:
                    self.move(coupSimule, board=b2,isPlaying=isPlaying)
                    #there is a other move that does'nt starve the opponent
                    print("Try : " + str(coupSimule) + " instead of " + str(pit))
                    print(b2)
                    if not(b2.emptySide(1-isPlaying)):
                        raise StarvationError() #so the move is not licit

            #It means the move has to be played but it ends the game
            return "END" 
        except NotInYourSideError as e:
            #print(e,file=sys.stderr)
            return False
        except EmptyPitError as e:
            print(e,file=sys.stderr)
            return False
        except StarvationError as e:
            print(e,file=sys.stderr)
            return False

    def play(self, pit):
        """Function to use in order to play a move on the Board
        It takes one argument : number of the pit wanted to be played"""
        if pit == "END":
            return "END"
        else:
            self.move(pit)
            return True

    def move(self,pit,board=None, isPlaying=None):
        """Function moving the seeds on the board and
        It takes one argument : number of the last pit visited
        returns number of seeds captured"""
        if board is None:
            board = self.b
        if isPlaying is None:
            isPlaying = self.isPlaying

        pit += 6 * isPlaying
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
        while (6*(1-isPlaying) <= p <= 5+6*(1-isPlaying)) and (2 <= board.getPit(p) <= 3):    
            seedsEaten += board.getPit(p)
            board.setPit(p,0)
            p -= 1

        # we only update the loft and the player if it's a play on the real board
        # we shouldn't move the seed on the board if we force the player
        if board == self.b and isPlaying == self.isPlaying:   
            self.whoIsPlaying().addToLoft(seedsEaten)
            self.isPlaying = 1 - self.isPlaying

        return seedsEaten

    def whoIsPlaying(self):
        if self.isPlaying == 0:
            return self.player0
        else:
            return self.player1

    def endOfGame(self):
        print(self.b)
        if self.player0.loft > self.player1.loft: #return nb of the inner
            return self.player0
        elif self.player0.loft < self.player1.loft:
            return self.player1
        else:
            return None

    def endGameIsBlocked(self):
        if self.b.board == [1,0,0,0,0,0,1,0,0,0,0,0]:
            self.player0.addToLoft(1)
            self.player1.addToLoft(1)
            self.b = [0]*12
            return True
        return False

class Board:
    def __init__(self):
        self.board = [4 for i in range(12)]

    def __repr__(self):
        s="  ====================J1=================\n"
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
        s+="|\n  ====================J0================="
        return s

    def getPit(self, k):
        return self.board[k]

    def setPit(self, k, val):
        self.board[k] = val

    def addPit(self, k, val):
        self.board[k] += val

    def emptySide(self,player):
        """Function looking if the side which first pit is ps is empty
        It takes one argument : ps"""
        for k in range(6*player, 6*player+6):
            if self.getPit(k) != 0:
                return False
        return True
