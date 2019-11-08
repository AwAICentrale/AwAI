# MTCS
from multiprocessing import Pool
from tqdm import tqdm
from random import randrange
import copy
import math


class Eval:
    def __init__(self, game, n=1000, n_seeds_end=10):
        """Paramaters : game, number of games tested"""
        self.game = game
        self.n = n  # number of games tested
        self.n_seeds_end = n_seeds_end
        self.ratio = [0, 0]
        self.list_bar = []  # useful for progess bar
        self.pbar = None
        # self.pbar = tqdm(total=self.n)

    def calculate_ratio(self):
        p = Pool()
        with tqdm(total=self.n) as pbar:
            for w in p.imap_unordered(self.random_game, range(self.n)):
                pbar.update()
                if w is not None:  # there is a winner, no equality
                    self.ratio[w] += 1 / self.n
        p.close()
        p.join()

    def random_game(self, list_bar):
        g = copy.deepcopy(self.game)
        g.set_players("alea", "alea")
        winner = g.run_game()  # toPrint=False)
        # print("Winner ->" , winner)
        if g.player0.loft > g.player1.loft:  # return nb of the winner
            return 0
        elif g.player0.loft < g.player1.loft:
            return 1


class Node:
    def __init__(self, pit, game):
        """Node object, takes 3 arguments : board, algorithm to calculate probabilities and n = sample size"""
        self.pred = None  # father Node
        self.succ = [None] * 6  # list of Nodes
        self.game = game
        self.n = 0  # number of times the node has been visited
        self.t = 0  # total number of simulation
        self.pit = pit  # pit that corresponds to the pit on the board
        self.is_a_leaf = True

    def expend(self):
        list_move = [0, 1, 2, 3, 4, 5]
        while list_move:
            move_test = list_move.pop(randrange(0, len(list_move)))
            result = self.game.allowed(move_test)
            # print(f"Move {move_test}, allowed {result}")
            if result:  # it is a valid move
                dg = copy.deepcopy(self.game)
                dg.play(move_test)
                n = Node(move_test, dg)
                n.pred = self  # predecessor is the node expending
                self.succ[move_test] = n
                self.is_a_leaf = False


class MCTS:
    def __init__(self, game, depth, nb_eval, constant):
        self.game = game
        self.tree_root = Node("Root", self.game)
        self.nb_eval = nb_eval
        self.depth = depth
        self.constant = constant

    def UCB1(self, node):
        if node.n != 0 and node.pred.n != 0:
            v_i = node.pred.t / node.pred.n
            return v_i + self.constant * math.sqrt(math.log(node.pred.n) / node.n)
        elif node.n != 0 and node.pred.n == 0:
            return node.pred.t / node.pred.n
        else:
            return float("inf")

    def expansion(self, node=None):
        if node is None:
            node = self.tree_root
        print(f"expending from node {node.pit}")

        if not node.is_a_leaf:  # this node has children
            iMax = None
            max = -1
            for i in range(6):
                if node.succ[i] is not None:
                    ucb1Node = self.UCB1(node.succ[i])
                    # print(f"Node {i} scores {ucb1Node}")
                    if ucb1Node > max:
                        iMax = i
                        max = ucb1Node
            # print(f"Node ucb1 max {iMax}")
            self.expansion(node.succ[iMax])
        else:
            if node.n == 0:
                self.rollout(node)
            else:
                node.expend()
                for i in range(6):
                    if node.succ[i] is not None:
                        self.rollout(node.succ[i])
                        break

    def rollout(self, node):
        # print(f"Rollout from node {node.pit}")

        e = Eval(node.game, self.nb_eval)
        e.calculate_ratio()
        t = e.ratio[self.game.is_playing]  # evaluation done when its your turn to play
        self.backpropagation(node, t)

    def backpropagation(self, node, t):
        print(f"backpropagation from node {node.pit}")
        node.n += 1
        node.t += t
        if node.pred is not None:  # we have to backpropagate again, still not the root of the tree
            self.backpropagation(node.pred, t)


class MCTSPlayer:
    def __init__(self, game, nb_eval=100, depth=19, constant=2):
        self.game = game
        self.nb_eval = nb_eval
        self.depth = depth
        self.constant = constant

    def play(self):
        mcts = MCTS(self.game, self.nb_eval, self.depth, self.constant)
        for _ in range(self.depth):
            mcts.expansion()
        # return indices of better move (that's hell)
        succ = [node for node in mcts.tree_root.succ if node is not None]
        if succ:
            succ_n = [node.n for node in succ]
            print(succ_n)
            move = succ[succ_n.index(max(succ_n))].pit
            return move
        else:
            return "END"
