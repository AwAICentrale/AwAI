import random
from src.tests import TestAmelioration


class Amelioration():
    def __init__(self, nb_generation, size_population, nb_gains, stage=None, proba_mutation=0.01, proba_cross=0.3):
        self.nb_generation = nb_generation
        self.nb_gains = nb_gains
        self.size_population = size_population
        self.adn = ADN(size_population, nb_gains, proba_mutation, proba_cross)
        self.stage = stage

    def amelioration(self):
        self.update_score()
        for i in range(self.nb_generation):
            self.adn.list_coeff_init.sort(key=lambda tup: tup[1], reverse=True)
            self.adn.selection()
            self.adn.cross()
            self.adn.mutation()

            self.update_score()
        self.adn.list_coeff_init.sort(key=lambda tup: tup[1], reverse=True)
        return self.adn.list_coeff_init

    def update_score(self):
        self.adn.list_coeff_init.sort(key=lambda tup: tup[1], reverse=True)
        for (i, (list_coeff_gain, score)) in enumerate(self.adn.list_coeff_init[1:]):
            game_test = TestAmelioration("alphabeta", "alphabeta", 1, self.stage, self.adn.list_coeff_init[0][0],
                                         list_coeff_gain)
            game_test.run()
            # update score
            self.adn.list_coeff_init[i][1] = game_test.game.player0.loft - game_test.game.player1.loft
            # is it the best way to evaluate the score ? 27 - 12 equivalent to 25 - 10 ?


class ADN:
    def __init__(self, size_population, nb_gains, proba_mutation, proba_cross):
        # create a set of initials solutions ; solutions used by minimax ab
        self.list_coeff_init = []
        self.size_population = size_population
        self.nb_gains = nb_gains
        self.proba_mutation = proba_mutation  # hig bound of genetic algorithm advice on wikipedia [0.001, 0.01]
        self.proba_cross = proba_cross  # pick randomly :)

        for i in range(size_population):
            liste_coeff_gain = []
            for j in range(nb_gains):
                sign = random.choice([-1, 1])
                liste_coeff_gain.append(sign * random.random())
            self.list_coeff_init.append([liste_coeff_gain, -float('inf')])

    def selection(self):  # select the solutions with the better scores and duplicate them
        self.list_coeff_init.sort(key=lambda tup: tup[1], reverse=True)
        n = self.size_population // 2
        self.list_coeff_init = self.list_coeff_init[:self.size_population - n] + [
            self.list_coeff_init[self.size_population - n + k] for k in range(n)]

    def mutation(self):  # some coeff mutate
        for k in range(self.size_population):
            for i in range(self.nb_gains):
                r = random.random()
                if r < self.proba_mutation:
                    sign = random.choice([-1, 1])
                    self.list_coeff_init[k][0][i] = sign * random.random()

    def cross(self):  # we choose 2 solutions, we replace them by crossing of themselves
        self.list_coeff_init.sort(key=lambda tup: tup[1], reverse=True)
        n = self.size_population // 2

        def repartition(length):  # handles which gen comes from which genitor
            a = []
            b = []
            for k in range(length):
                rand = random.random()
                if rand < 0.5:
                    a.append(k)
                else:
                    b.append(k)
            return a, b

        for i, (papa, mama) in enumerate(zip(self.list_coeff_init[:n], self.list_coeff_init[n:])):
            r = random.random()
            if r < self.proba_cross:
                son1 = [0] * self.nb_gains
                son2 = [0] * self.nb_gains

                a, b = repartition(self.nb_gains)

                for ind in a:
                    son1[ind] = papa[0][ind]
                    son2[ind] = mama[0][ind]

                for ind in b:
                    son1[ind] = mama[0][ind]
                    son2[ind] = papa[0][ind]

                self.list_coeff_init[i] = [son1, -float('inf')]
                self.list_coeff_init[i + n] = [son2, -float('inf')]
