from src.engine import *
from tqdm import tqdm
from multiprocessing import Pool
import numpy as np
import psutil
import time


class Test:
    """This class is meant to be the class that provides the tests between the IAs
    You shall provide the name of the two algorithms you want to get stats on"""

    def __init__(self, algo0, algo1, nb_games, data0=None, data1=None):
        self.nb_games = nb_games
        self.stat = [0, 0, 0]
        self.algo0 = algo0
        self.algo1 = algo1
        self.data0 = data0
        self.data1 = data1

    def run(self):
        start = time.time()
        for _ in tqdm(range(self.nb_games)):
            self.game = Game()
            self.game.set_players(self.algo0, self.algo1, self.data0, self.data1)
            winner = self.game.run_game()
            if winner == self.game.player0:
                self.stat[0] += 1
            elif winner == self.game.player1:
                self.stat[1] += 1
            else:
                self.stat[2] += 1
        duration = time.time() - start
        print(f"The calculus has taken {duration}s.")
        return np.array(self.stat).sum(axis=0)

    def run_on_cpu(self, n):
        stat = [0, 0, 0]
        self.game = Game()
        self.game.set_players(self.algo0, self.algo1, self.data0, self.data1)
        winner = self.game.run_game()
        if winner == self.game.player0:
            stat[0] += 1
        elif winner == self.game.player1:
            stat[1] += 1
        else:
            stat[2] += 1
        # print(f"game : {n}"
        # print(self.game.player0.loft, self.game.player1.loft)
        return stat

    def run_on_all_cores(self):
        start = time.time()
        print("Start calculus")
        nb_cpus = psutil.cpu_count()
        p = Pool(nb_cpus)
        self.stat = []
        with tqdm(total=self.nb_games) as pbar:
            for stat in p.imap_unordered(self.run_on_cpu, range(self.nb_games)):
                pbar.update()
                self.stat.append(stat)
        p.close()
        p.join()

        print("End main process")
        duration = time.time() - start
        self.stat = np.array(self.stat).sum(axis=0)
        print(f"The calculus has taken {round(duration, 2)}s.")

    def __repr__(self):
        return f"algo {self.game.player0.algo: s} : {self.stat[0]: f} % \n \
                    algo {self.game.player1.algo: s} : {self.stat[1]: f} % \n \
                    tied : {self.stat[2]: f} % "
