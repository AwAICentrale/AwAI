import random as rd
import copy

class Board:
    def __init__(self):
        self.board = [4 for i in range(12)]
        self.player = 0
        self.grenier = [0,0]

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

    def play(self,pit):
        """Function to use in order to play a move on the Board
        It takes one argument : number of the pit wanted to be played"""
        rslt=self.allowed(pit)
        if rslt=="END":
            return "END"
        elif rslt == False:
            return None
        else:
            return self.move(pit)



    def allowed(self, pit):
        """Function checking if the move is licit or not
        Takes one arguments : number of the pit wanted to be played
        """
        if (pit not in range(1,7)) or self.board[pit-1+6*self.player]==0: # Pit not included in [1,6] or pit wanted is empty
            return False
        cb = copy.deepcopy(self)
        cb.move(pit)#We play
        if not cb.emptySide(6*(cb.player)): #if opponent's side is not empty
            return True
        else : # we need to know if there are licit moves
            for coupSimule in range(1, 7):
                db = copy.deepcopy(self) #For move we do a copy of the board (we don't want to change the original board)
                if coupSimule != pit: # moves different from pit
                    db.move(coupSimule)
                    if not(db.emptySide(6*db.player)):    #there is a other move that does'nt starve the opponent
                        return False                    #so the move is not licit
                return "END" #It means the move has to be played but it ends the game
        return True

    def move(self,pit):
        """Function moving the seeds on the board and
        It takes one argument : number of the last pit visited
        returns number of seeds captured"""

        pit = pit-1+6*self.player
        nbSeeds = self.board[pit]       #saving the number of seeds to sow
        self.board[pit] = 0
        p0 = pit
        while nbSeeds > 0:
            p0 = (p0 + 1)%12
            if p0 != pit:           #We don't put any seeds in the starting pit
                self.board[p0] += 1
                nbSeeds-=1
        sG= self.seedsGain(p0)    #
        self.grenier[self.player] +=sG
        self.player = 1 -self.player
        return sG

    def seedsGain(self,lastPit):
        """Function deleting all seeds captured by a player
        It takes one argument : number of the last pit visited
        returns the number of seeds captured"""
        seeds=0
        while (6*(1-self.player) <= lastPit <= 5+6*(1-self.player)) and (2 <= self.board[lastPit] <= 3):    # Last seeds is indeed in opponent's side and there is 2 or 3 seeds in the pit
            seeds += self.board[lastPit]
            self.board[lastPit] = 0
            lastPit -= 1
        return seeds


    def emptySide(self,ps):
        """Function looking if the side which first pit is ps is empty
        It takes one argument : ps"""
        for k in range(ps, ps+6):
            if self.board[k] != 0:
                return False
        return True


class Minimax:
    def __init__(self,board,listFGain,listCoeffGain):
        self.board = board
        if len(listFGain)!=len(listCoeffGain):
            return None
        self.listFGain=listFGain
        self.listCoeffGain=listCoeffGain

    def minimax(self):
        bestMove=0
        hGain=float("-inf")
        lGain = len(self.listFGain)*[0]
        for moveA in range(1,7): #we try every move possible
            gainMoveA=float("inf")
            b=copy.deepcopy(self.board) #Copy of the board in order not to change the original one
            if b.play(moveA)not in [None,"END"]:
                for moveB in range(1,7):
                    gainMoveAB=float("inf")
                    b2=copy.deepcopy(b)
                    if b2.play(moveB)not in [None,"END"]: #Move A and B are licit then we calculate the gain
                        gainMoveAB=self.gain(moveA,moveB)
                    if gainMoveAB<gainMoveA:
                        gainMoveA=gainMoveAB
            if gainMoveA!=float("inf"):
                if gainMoveA>hGain:
                    hGain=gainMoveA
                    bestMove=moveA
        return bestMove

    def gainA(self,board,moveA,moveB):
        return board.play(moveA)

    def gainB(self,board,moveA,moveB):
        #print("Move A : ",moveA)
        board.play(moveA)
        return -board.play(moveB)

    def gain(self,moveA,moveB):
        dictGain = {"gainA":self.gainA,"gainB":self.gainB}
        g=0
        for i in range(len(self.listFGain)):
            bCopyGain=copy.deepcopy(self.board) #For each gain we do a copy of the board (we don't want to change the original board during gain calculus)
            g+=self.listCoeffGain[i]*dictGain[self.listFGain[i]](bCopyGain,moveA,moveB)
        return g

class Game:
    def __init__(self,nbSeedsEnd=8):
        self.b = Board()
        self.m = Minimax(self.b,["gainA","gainB"],[1,1])
        self.nbSeedsEnd=nbSeedsEnd

    def runGame(self):
        while sum(self.b.grenier)<48-self.nbSeedsEnd and max(self.b.grenier[0],self.b.grenier[1])<=24:
            print(self.b)
            notInt=True
            while notInt:
                answ = input("Move : ")
                if answ =="quit":
                    return False
                try:
                    pit=int(answ)

                    notInt=False
                except: pass
            rsltMove = self.b.play(pit)
            if rsltMove =="END":
                self.b.grenier[self.b.player]+=(48-sum(self.b.grenier))
            elif rsltMove !=None:
                print(self.b)
                input()
                pitComp=self.m.minimax()
                print("Computer plays ",pitComp)
                self.b.play(pitComp)
                print("Score  :",self.b.grenier[0],self.b.grenier[1])
            else:
                print("Move not allowed")
        print(self.b)
        return self.b.grenier.index(max(self.b.grenier)) #return nb of the winner

class GameMinimaxVSMinimax:
    def __init__(self,lGain,lGain2,listeCoeff,listeCoeff2,nbSeedsEnd=8):
        self.b = Board()
        self.m1 = Minimax(self.b,lGain,listeCoeff)
        self.m2 = Minimax(self.b,lGain2,listeCoeff2)
        self.nbSeedsEnd=nbSeedsEnd

    def runGame(self):
        i=0
        while sum(self.b.grenier)<48-self.nbSeedsEnd and max(self.b.grenier[0],self.b.grenier[1])<=24:
            #print(self.b)
            pitComp=self.m1.minimax()
            #print("Computer 1 plays ",pitComp)
            self.b.play(pitComp)
            #print("Score  :",self.b.grenier[0],self.b.grenier[1])
            pitComp=self.m2.minimax()
            #print("Computer 2 plays ",pitComp)
            self.b.play(pitComp)
            #print("Score  :",self.b.grenier[0],self.b.grenier[1])
        print(self.b)
        return self.b.grenier.index(max(self.b.grenier)) #return nb of the winner


class RandomPlay:
    def __init__(self,board):
        self.board = board

    def rdMove(self):
        listMove=[]
        for moveA in range(1,7): #we try every move possible
            b=copy.deepcopy(self.board) #Copy of the board in order not to change the original one
            rsltMove = b.play(moveA)
            if rsltMove =="END":
                self.board.grenier[self.board.player]+=(48-sum(self.board.grenier))
                #print("End of the game")
            if rsltMove!=None:
                for moveB in range(1,7):
                    b2=copy.deepcopy(b)
                    if b2.play(moveB)!=None: #Move A and B are licit then we add move A to the list of possible moves
                        listMove.append(moveA)
        if listMove==[]:
            return "Empty"
        return listMove[rd.randint(0,len(listMove)-1)]

class GameRdVSRd:
    def __init__(self,board,nbSeedsEnd=8): #the Board is an argument because we want to be able to use it even in the middle of the game
        self.b = board
        self.m1 = RandomPlay(self.b)
        self.m2 = RandomPlay(self.b)
        self.nbSeedsEnd=nbSeedsEnd

    def runGame(self):
        i=0
        while sum(self.b.grenier)<48-self.nbSeedsEnd and max(self.b.grenier[0],self.b.grenier[1])<=24:
            #print(self.b)
            pitComp=self.m1.rdMove()
            #print("Computer 1 plays ",pitComp)
            self.b.play(pitComp)
            #print(self.b)
            #print("Score  :",self.b.grenier[0],self.b.grenier[1])
            pitComp=self.m2.rdMove()
            #print("Computer 2 plays ",pitComp)
            self.b.play(pitComp)
            #print("Score  :",self.b.grenier[0],self.b.grenier[1])
        #print(self.b)
        return self.b.grenier.index(max(self.b.grenier)) #return nb of the winner
