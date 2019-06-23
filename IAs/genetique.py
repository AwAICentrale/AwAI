
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
            