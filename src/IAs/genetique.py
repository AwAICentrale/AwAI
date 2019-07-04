import random
from src.tests import Test


class Amelioration():
    def __init__(self, nbGeneration, taillePopulation, nbGains, probaMutation=0.01, probaCross=0.3):
        self.nbGeneration = nbGeneration
        self.nbGains = nbGains
        self.taillePopulation = taillePopulation
        self.adn = ADN(taillePopulation, nbGains, probaMutation, probaCross)

    def amelioration(self):
        self.majScore()
        for i in range(self.nbGeneration):
            self.adn.listeCoeffInit.sort(key=lambda tup: tup[1])
            self.adn.selection()
            self.adn.cross()
            self.adn.mutation()
            self.majScore()
        self.adn.listeCoeffInit.sort(key=lambda tup: tup[1])
        return self.adn.listeCoeffInit

    def majScore(self):
        self.adn.listeCoeffInit.sort(key=lambda tup: tup[1])
        for (listeCoeffGain, score) in self.adn.listeCoeffInit[1:]:
            gameTest = Test("alphabeta", "alphabeta", 1, self.adn.listeCoeffInit[0][0], listeCoeffGain)
            gameTest.run()
            score = gameTest.game.player0.loft - gameTest.game.player1.loft  # is it the best way to evaluate the score ?
            # 27 - 12 equivalent to 25 - 10 ?


class ADN:
    def __init__(self, taillePopulation, nbGains, probaMutation,
                 probaCross):  # crée un ensemble de solutions initiales : liste de coefficients pour minimaxAB
        self.listeCoeffInit = []
        self.taillePopulation = taillePopulation
        self.nbGains = nbGains
        self.probaMutation = probaMutation  # hig bound of genetic algorithm advice on wikipedia [0.001, 0.01]
        self.probaCross = probaCross  # pick randomly :)

        for i in range(taillePopulation):
            listeCoeffGain = []
            for j in range(nbGains):
                sign = random.choice([-1, 1])
                listeCoeffGain.append(sign * random.random())
            self.listeCoeffInit.append((listeCoeffGain, -float('inf')))

    def selection(self):  # sélectionne les solutions avec les scores les plus élevés et les duplique
        self.listeCoeffInit.sort(key=lambda tup: tup[1])
        n = self.taillePopulation // 2
        self.listeCoeffInit = [self.listeCoeffInit[self.taillePopulation - n + k] for k in range(n)]

    def mutation(self):  # certains coefficients mutent
        for k in range(self.taillePopulation):
            for i in range(self.nbGains):
                r = random.random()
                if r < self.probaMutation:
                    sign = random.choice([-1, 1])
                    self.listeCoeffInit[k][0][i] = sign * random.random()

    def cross(self):  # on choisit 2 solutions, on les remplace par des croisements de ces 2 solutions
        self.listeCoeffInit.sort(key=lambda tup: tup[1])
        n = self.taillePopulation // 2

        def repartition(longueur):  # gère de quel parent provient quel gène
            a = []
            b = []
            for k in range(longueur):
                r = random.random()
                if r < 0.5:
                    a.append(k)
                else:
                    b.append(k)
            return a, b

        for papa, mama in zip(self.listeCoeffInit[:n], self.listeCoeffInit[n:]):
            r = random.random()
            if r < self.probaCross:
                fils1 = [0] * self.nbGains
                fils2 = [0] * self.nbGains

                a, b = repartition(self.nbGains)

                for ind in a:
                    fils1[ind] = papa[0][ind]
                    fils2[ind] = mama[0][ind]

                for ind in b:
                    fils1[ind] = mama[0][ind]
                    fils2[ind] = papa[0][ind]

                self.listeCoeffInit[papa] = (fils1, -float('inf'))
                self.listeCoeffInit[mama] = (fils2, -float('inf'))
