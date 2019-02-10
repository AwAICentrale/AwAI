
#le board est numéroté:          les joueurs choisissent la case qu'ils jouent avec la numérotation classique suivante:
# 12 11 10  9  8  7                6  5  4  3  2  1
#  1  2  3  4  5  6                1  2  3  4  5  6


import random as rd
import copy
import time
import matplotlib.pyplot as plt


class Board:
    def __init__(self):
        self.board = [4 for i in range(12)]
        self.player = rd.randint(0,1)
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
        if not self.allowed(pit):
            print("Error, move not allowed")
            return False
        pit = pit-1+6*self.player
        nbSeeds = self.board[pit]       #on stocke le nb de graine à distribuer
        self.board[pit] = 0
        p0 = pit
        while nbSeeds > 0:
            p0 = (p0 + 1)%12        #on passe à la case suivante
            if p0 != pit:           #on ne joue pas dans la case où l'on a pris les graines
                self.board[p0] += 1     #on ajoute une graine
                nbSeeds-=1
        self.grenier[self.player] += self.seedsGain(p0)    #on renvoie le nombre de graines mangées (et on les retire)
        self.player = 1 -self.player
  

print(p)
print(p.grenier)
    def seedsGain(self,lastPit):  #supprime les graines mangées et renvoie le nombre de graines amassées
        seeds=0
        while (6*(1-self.player) <= lastPit <= 5+6*(1-self.player)) and (2 <= self.board[lastPit] <= 3):    #la dernière case que l'on a remplie est chez l'adversaire
            seeds += self.board[lastPit]
            self.board



            [lastPit] = 0
            lastPit -= 1
        return seeds

    def allowed(self, pit):   #fct regarde si coup possible qui n'affame pas l'adversaire et si correspond bien à [|1,6|]
        print(self.board[pit-1])
        if (pit not in range(1,7)) or self.board[pit-1+6*self.player]==0:
            return False
        if self.emptySide():                                 #l'adversaire est affamé
            for coupSimule in range(1, 7):
                db = copy.deepcopy(self) #On copie le plateau pour simuler les coups
                if coupSimule != pit-1: # correspond au coup déjà souhaité
                    db.play(coupSimule)
                    if not(db.emptySide()):    #il y a un coup qui n'affame pas l'adversaire
                        return False                    #le coup n'est pas légal
        return True                             #le coup est légal

    def emptySide(self):           #on regarde si le côté de l'adversaire est vide (pour regarder si le coup joué n'affame pas l'adversaire)
        ps= 6*(1-self.player)
        for k in range(ps, ps+6):              #on regarde si le côté est vide
            if self.board[k] != 0:
                return False
        return True
