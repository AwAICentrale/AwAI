# MTCS
import time
from multiprocessing import Pool
from queue import Queue
from tqdm import tqdm
from random import randint,randrange
import sys
import copy
import math
sys.path.append('../..')
from src.engine import *
from src.player import AI, Human

from src.AIs.minimax import Minimax
from src.AIs.alea import Alea
from src.AIs.alphabeta import AlphaBeta

class Eval:
    def __init__(self, game, n=1000,nSeedsEnd=10):
        """Paramaters : game, number of games tested"""
        self.game = game
        self.n = n
        self.nSeedsEnd = nSeedsEnd
        self.ratio = [0,0]
        self.pbar = None
        self.i=0
        self.l=[]
        self.l1=[]
        #self.pbar = tqdm(total=self.n)

    def calculateRatio(self):
        p=Pool()
        with tqdm(total=self.n) as pbar:
            for w in p.imap_unordered(self.randomGame, range(self.n)):
                pbar.update()
                if w!=None: # there is a winner, no equality
                    self.ratio[w]+=1/self.n
        p.close()
        p.join()


    def randomGame(self,l):
        g = copy.deepcopy(self.game)
        g.set_players("alea","alea")
        winner = g.run_game()#toPrint=False)
        #print("Winner ->" , winner)
        if g.player0.loft > g.player1.loft: #return nb of the winner
            return 0
        elif g.player0.loft < g.player1.loft:
            return 1

class Node:
    def __init__(self,pit,game):
        """Node object, takes 3 arguments : board, algorithme to calcule probabilities and n = sample size"""
        self.pred=None
        self.succ=[None]*6
        self.game=game
        self.n=0
        self.t=0
        self.pit=pit
        self.isALeaf = True

    def expend(self):
        listMove = [0,1,2,3,4,5]
        while listMove != []:
            moveTest = listMove.pop(randrange(0,len(listMove)))
            rslt = self.game.allowed(moveTest)
            #print(f"Move {moveTest}, allowed {rslt}")
            if rslt: # it is a valid move
                dg = copy.deepcopy(self.game)
                dg.play(moveTest)
                n = Node(moveTest,dg)
                n.pred=self #predecessor is the node expending
                self.succ[moveTest]=n
                self.isALeaf=False




class MCTS:
    def __init__(self,game,player,nEval=1000):
        self.game = game
        self.treeRoot=Node("Root",self.game)
        self.player= player
        self.nEval=nEval


    def UCB1(self, node, constant = 2):
        if node.n != 0 and node.pred.n!=0:
            v_i = node.pred.t/node.pred.n
            return v_i + constant*math.sqrt(math.log(node.pred.n)/node.n)
        elif node.n == 0 and node.pred.n==0:
            return node.pred.t/node.pred.n
        else:
            return float("inf")

    def expansion(self, node = None):
        if node == None :
            node = self.treeRoot
        print(f"expending from node {node.pit}")

        if not node.isALeaf: # this node has children
            iMax=None
            max = -1
            for i in range(6):
                if node.succ[i]!=None:
                    ucb1Node = self.UCB1(node.succ[i])
                    #print(f"Node {i} scores {ucb1Node}")
                    if ucb1Node > max:
                        iMax = i
                        max = ucb1Node
            #print(f"Node ucb1 max {iMax}")
            self.expansion(node.succ[iMax])
        else:
            if node.n == 0:
                self.rollout(node)
            else:
                node.expend()
                for i in range(6):
                    if node.succ[i]!=None:
                        self.rollout(node.succ[i])
                        break

    def rollout(self,node):
        #print(f"Rollout from node {node.pit}")

        e = Eval(node.game,self.nEval)
        e.calculateRatio()
        t = e.ratio[self.game.is_playing] # evaluation done when its your turn to play
        self.backpropagation(node,t)

    def backpropagation(self,node,t):
        print(f"backpropagation from node {node.pit}")
        node.n +=1
        node.t += t
        if node.pred != None: #we have to backpropagate again, still not the root of the tree
            self.backpropagation(node.pred,t)








g = Game()
g.set_players("human","human")
g.is_playing = 0
g.nb_seeds_eaten = 4
b= Board()
b.board = [4,5,5,5,5,0,4,4,4,4,4,4]
g.b = b
m=MCTS(g,0)
for i in range(20):
    m.expansion()


# if __name__ == "__main__":
#     g = Game()
#     g.is_playing = 1
#     g.nb_seeds_eaten = 4
#     b= Board()
#     b.board = [4,5,5,5,5,0,4,4,4,4,4,4]
#     g.board = b
#     e = Eval(g,10000)
#     e.calculateRatio()
#     print("Le score est {}/{}".format(round(e.ratio[0],3),round(e.ratio[1],3)))
