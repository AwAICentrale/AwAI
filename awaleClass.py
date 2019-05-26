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
    
    
    def minimaxAB(self, depth, alpha, beta, maximizingPlayer, listCoeffGain):
        if (depth == 0) or (self.board.grenier[0] >= 24) or (self.board.grenier[1] >= 24):
            return self.gainMAB(listCoeffGain), -1
        
        bestMove = -1
        
        if maximizingPlayer:
            maxEval = -float('inf')
            for move in range(1, 7):
                MinimaxCopy = copy.deepcopy(self)
                if MinimaxCopy.board.play(move) not in [None, "END"]:
                    eval, m = MinimaxCopy.minimaxAB(depth-1, alpha, beta, False, listCoeffGain)
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = move
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval, bestMove
        
        else:
            minEval = float('inf')
            for move in range(1, 7):
                MinimaxCopy = copy.deepcopy(self)
                if MinimaxCopy.board.play(move) not in [None, "END"]:
                    eval, m = MinimaxCopy.minimaxAB(depth-1, alpha, beta, True, listCoeffGain)
                    if eval < minEval:
                        minEval = eval
                        bestMove = move
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval, bestMove
                
    def gainMAB(self, listCoeffGain):
        a, b, c, d = listCoeffGain
        gain = self.gainMAB0() + a*self.gainMAB1() + b*self.gainMAB2() + c*self.gainMAB3() + d*self.gainMAB4()
        return gain
    
    def gainMAB0(self):
        if self.board.grenier[self.board.player] >= 24:
            return float('inf')
        elif self.board.grenier[1-self.board.player] >= 24:
            return -float('inf')
        else:
            return 0
    
    def gainMAB1(self):     #return our wined seeds
        return self.board.grenier[self.board.player]/23     #23 max score
    
    def gainMAB2(self):     #return our loosed seeds
        return self.board.grenier[1-self.board.player]/23   #23 max score
    
    def gainMAB3(self):     #count 1 or 2 seeds
        gain = 0
        successive = 1      #count the number of 1 or 2 seeds in a row
        opponent = 1-self.board.player
        for pit in range(6*self.board.player, 6+6*self.board.player):
            sbp = self.board.board[pit]
            if (sbp == 1) or (sbp == 2):
                gain -= 12*sbp*successive
                successive += 1
            else:
                successive = 1
        for pit in range(6*opponent, 6+6*opponent):
            sbp = self.board.board[pit]
            if (sbp == 1) or (sbp == 2):
                gain += 8*sbp*successive    #opponent play first
                successive += 1
            else:
                successive = 1
        return gain/504     #504 max score {12*[(2*1)+(2*2)+...+(2*6)]}
         
    def gainMAB4(self):     #possible moves
        gain = 0
        opponent = 1-self.board.player
        for pit in range(6*self.board.player, 6+6*self.board.player):
            if self.board.board[pit] > 0:
                gain += 1
        for pit in range(6*opponent, 6+6*opponent):        
            if self.board.board[pit] > 0:
                gain -= 1
        return gain/5   #5 max score {+6 -1}
    
    

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


class GameMinimaxABVSPlayer:
    def __init__(self,lGain,listCoeffGain):
        self.b = Board()
        self.m1 = Minimax(self.b, [], listCoeffGain)
        self.list = listCoeffGain

    def runGame(self):
        i=0
        depth = 6
        while max(self.b.grenier[0],self.b.grenier[1])<=24:           
            if self.b.player == 1:
                print()
                print("tour de l'ordi : ")
                print("ordi : ", self.b.grenier[1], " vous : ", self.b.grenier[0])
                print(repr(self.b))
                gain, pitComp = self.m1.minimaxAB(depth, -float('inf'), float('inf'), True, self.list)
                print("coup : ", pitComp)
                self.b.play(pitComp)
            else:
                print()
                print("votre tour : ")
                print("ordi : ", self.b.grenier[1], " vous : ", self.b.grenier[0])
                print(repr(self.b))
                move = -1
                while move not in [1, 2, 3, 4, 5, 6]:
                    print("Donnez un coup entre 1 et 6 : ")
                    move = int(input(""))
                self.b.play(move)
                
            
        print(self.b)
        return self.b.grenier.index(max(self.b.grenier)) #return nb of the winner

class GameMinimaxABVSMinimaxAB:
    def __init__(self,lGain,lGain2,listeCoeff,listeCoeff2,nbTurn=60):
        self.b = Board()
        self.m1 = Minimax(self.b,lGain,listeCoeff)
        self.m2 = Minimax(self.b,lGain2,listeCoeff2)
        self.l1 = listeCoeff
        self.l2 = listeCoeff2
        self.nbTurn = nbTurn

    def runGame(self):
        i=0
        depth = 6
        while i<self.nbTurn//2 and max(self.b.grenier[0],self.b.grenier[1])<=24:
#            print(self.b.grenier[0], self.b.grenier[1])
#            print(repr(self.b))
            gain, pitComp=self.m1.minimaxAB(depth, -float('inf'), float('inf'), True, self.l1)
            self.b.play(pitComp)
#            print(self.b.grenier[0], self.b.grenier[1])
#            print(repr(self.b))
            gain, pitComp=self.m2.minimaxAB(depth, -float('inf'), float('inf'), True, self.l2)
            self.b.play(pitComp)
            i += 1
        sbg1 = self.b.grenier[0]
        sbg2 = self.b.grenier[1]
        print(sbg1, sbg2)
        if sbg1 > sbg2:
            return self.l1, sbg1, sbg2
        else:
            return self.l2, sbg2, sbg1
        
        #return self.b.grenier.index(max(self.b.grenier)) #return nb of the winner

class Amelioration():
    def __init__(self, taillePopulation):
        self.b = Board()
        self.sol = AlgoGenetique(taillePopulation)
        
    def amelioration(self, nbGeneration):
        self.sol.triRapide()
        listeCoeff0 = self.sol.pop[0][0]
        for indSolution in range(1, self.sol.tllPop):
            gmm = GameMinimaxABVSMinimaxAB([], [], listeCoeff0, self.sol.pop[indSolution][0])
            lstCoef, score1, score2 = gmm.runGame()
            if lstCoef == listeCoeff0:
                delta = score2 - score1
            else:
                delta = score1 - score2
            self.sol.pop[indSolution] = (self.sol.pop[indSolution][0], max(score1, score2)*delta) 
        for i in range(nbGeneration-1):
            self.sol.triRapide()
            listeCoeff0 = self.sol.pop[0][0]
            #for indSolution in range(1, self.sol.tllPop):
            self.sol.selection()
            self.sol.croisement()
            self.sol.mutation()
            for indSolution in range(1, self.sol.tllPop):
                gmm = GameMinimaxABVSMinimaxAB([], [], listeCoeff0, self.sol.pop[indSolution][0])
                lstCoef, score1, score2 = gmm.runGame()
                if lstCoef == listeCoeff0:
                    delta = score2 - score1
                else:
                    delta = score1 - score2
                self.sol.pop[indSolution] = (self.sol.pop[indSolution][0], score1*delta)    
        self.sol.triRapide()
        print(self.sol.pop[0][0])
        return self.sol.pop

class AlgoGenetique:
    def __init__(self, taillePopulation):   #crée un ensemble de solutions initiales : liste de coefficients pour minimaxAB
        listeCoeffinit = []
        for i in range(taillePopulation):
            l = []
            for j in range(4):
                signe = 1-rd.randint(0, 1)*2
                l.append(signe*rd.random())
            listeCoeffinit.append((l, -float('inf')))
        self.tllPop = taillePopulation
        self.pop = listeCoeffinit
            
    def triRapide(self):
        def trirap(self, g, d):
            pivot = self.pop[(g+d)//2][1]
            i = g
            j = d
            while True:
                while self.pop[i][1]>pivot:
                    i+=1
                while self.pop[j][1]<pivot:
                    j-=1
                if i>j:
                    break
                if i<j:
                    self.pop[i], self.pop[j] = self.pop[j], self.pop[i]
                i+=1
                j-=1
            if g<j:
                trirap(self , g, j)
            if i<d:
                trirap(self, i, d)
        g=0
        d=self.tllPop-1
        trirap(self, g, d)

    def selection(self):    #sélectionne les solutions avec les scores les plus élevés et les duplique
        self.triRapide()
        n = self.tllPop//2
        for k in range(n):
            sol = copy.deepcopy(self.pop[k])
            self.pop[self.tllPop-n+k] = sol
        
    def mutation(self):     #certains coefficients mutent
        proportion = 0.01
        for k in range(self.tllPop):
            l = len(self.pop[0][0])
            for i in range(l):
                r = rd.random()
                if r < proportion:
                    signe = 1-rd.randint(0, 1)*2
                    self.pop[k][0][i] = signe*rd.random()

    def croisement(self):   #on choisit 2 solutions, on les remplace par des croisements de ces 2 solutions
        self.triRapide()
        proportion = 0.3
        n = self.tllPop//2
        l = len(self.pop[0][0])
        def repartition(longueur):  #gère de quel parent provient quel gène
            a = []
            b = []
            for k in range(longueur):
                r = rd.random()
                if r < 0.5:
                    a.append(k)
                else:
                    b.append(k)
            return a, b
        for i in range(n):
            r = rd.random()
            if r < proportion:
                fils1 = [0]*l
                fils2 = [0]*l
                j = i+n
                a, b = repartition(l)
                for ind in a:
                    fils1[ind] = self.pop[i][0][ind]
                    fils2[ind] = self.pop[j][0][ind]
                for ind in b:
                    fils1[ind] = self.pop[j][0][ind]
                    fils2[ind] = self.pop[i][0][ind]
                self.pop[i] = (fils1, -float('inf'))
                self.pop[j] = (fils2, -float('inf'))
            
            
S = AlgoGenetique(10)
S.pop = [([0.5368739981532591, 0.5877779258598409, 0.16994777324658894, 0.9082132447942338], -4), ([0.8559695133840701, 0.8561372628064281, 0.9992500657384864, 0.13127204232122658], -1.2), ([0.35891716788954664, 0.7505148781116142, 0.540043606363959, 0.1571397109444318], 0), ([0.7022874605572366, 0.04551764190485752, 0.2355047997447388, 0.06028786634610539], 0.1), ([0.49330525558797966, 0.10174415803142045, 0.5802266272953037, 0.8573240738490336], 1.42), ([0.9905172925917508, 0.023719921879966965, 0.7239651329407082, 0.9946542517861322], 1.44), ([0.028424161995937114, 0.4191967419272443, 0.5498982961318426, 0.5072704599473227], 2), ([0.6713224307184147, 0.4153300432105721, 0.7132802912103343, 0.6256436342138162], 8), ([0.7513928538134895, 0.8906785224674364, 0.6640220421764618, 0.4070851747786933], 10), ([0.7455263167716993, 0.44784538684545816, 0.3690064112424436, 0.7145500880962735], 144)]        

#meilleure: l9           
l = [0.5160124471418471, 0.43951189430682513, 0.4732563569129571, 0.0826670380317569]
l2 = [0.30357221102322207, 0.7050237299399793, 0.11545859390594393, 0.3438369007184222]
l3 = [0.7466605777969665, 0.5374916400940779, 0.35383959746708105, 0.7298077100834444]

l4 = [0.7393321304544394,0.07044216317516239,0.3855292135159287,0.9459660639000087]
l5 = [0.7393321304544394,0.2974839386409064,0.3855292135159287,0.9924093364227078]
l6 = [0.8232960080599223,0.2673880927145049,0.3855292135159287,0.9459660639000087]
l7 = [0.8232960080599223,0.40095145595735293,0.5126913216106566,0.9833239456846349]

l8 = [1, -1, 0.5, 0.3]

l9 = [0.676061829383705, -0.4604896125458653, 0.7408590076155085, 0.3691310747575154]

l10 = [0.6141082049518831, -0.419252543918735, -0.14667859159770857, 0.8364893340278999]