from tqdm import tqdm
from engine import Game, Board




class Eval:
    def __init__(self, game, n=1000,nSeedsEnd=10):
        """Paramaters : game, number of games tested"""
        self.gameInit = game
        self.n = n
        self.nSeedsEnd = nSeedsEnd
        self.ratio = [0,0]


    def calculateRatio(self):
        self.ratio = [0,0]

        for i in tqdm(range(self.n)):
            self.g = Game(self.nSeedsEnd)
            self.g.isPlaying = self.gameInit.isPlaying
            self.g.nbSeedsEaten = self.gameInit.nbSeedsEaten

            self.g.setPlayers("random","random")
            self.g.runGame(toPrint=False)
            if self.g.player0.loft > self.g.player1.loft: #return nb of the winner
                self.ratio[0]+=(1/self.n)
            elif self.g.player0.loft < self.g.player1.loft:
                self.ratio[1]+=(1/self.n)



g = Game()
g.setPlayers("humain","humain")
g.isPlaying = 1
g.nbSeedsEaten = 4
b= Board()
b.board = [4,5,5,5,5,0,4,4,4,4,4,4]
g.board = b

e = Eval(g,10000)
e.calculateRatio()
print("Le score est {}/{}".format(round(e.ratio[0],3),round(e.ratio[1],3)))
