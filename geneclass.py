import random
import operator

class genalg:

    def __init__(self, password, sizepop = 100, propvp = 0.5, propmut = 0.4):
        self.password = password
        self.lenpass = len(password)
        self.sizepop = sizepop
        self.propvp = propvp
        self.propmut = propmut
        self.firstGen = True
        self.gen = []

    def fitness(self, palavrateste):
        score = 0
        i = 0
        while (i < self.lenpass):
            if (self.password[i] == palavrateste[i]):
                score+=1
            i+=1
        return score * 100 / self.lenpass

    def geraPal(self):
    	i = 0
    	result = ""
    	while i < self.lenpass:
    		letter = chr(97 + int(26 * random.random()))
    		result += letter
    		i +=1
    	return result

    def firstPop(self):
        population = []
        i = 0
        while i < self.sizepop:
            population.append(self.geraPal())
            i+=1
        return population

    def fitPop(self, popu = False):
        populationPerf = {}
        if(self.firstGen == True):

            popu = self.firstPop()

        else:

            popu = self.gen

        for individual in popu:
            populationPerf[individual] = self.fitness(individual)

        return sorted(populationPerf.items(), key = operator.itemgetter(1), reverse=True)

    def selectPop(self):
        nextGeneration = []
        popSorted = self.fitPop()
        nBest = int(self.sizepop * self.propvp)
        nWorst =  self.sizepop - nBest
        for i in range(nBest):
            nextGeneration.append(popSorted[i][0])
        for i in range(nWorst):
            nextGeneration.append(random.choice(popSorted)[0])
        random.shuffle(nextGeneration)
        return nextGeneration

    def child(self, ind1, ind2):
    	child = ""
    	for i in range(len(ind1)):
    		if (int(100 * random.random()) < 50):
    			child += ind1[i]
    		else:
    			child += ind2[i]
    	return child

    def children(self):
        nextPopulation = []
        breeders = self.selectPop()
        for i in range(int(len(breeders)/2)):
            for j in range(self.sizepop):
                nextPopulation.append(self.child(breeders[i], breeders[len(breeders) -1 -i]))
        return nextPopulation

    def mutacao(self, palavra):
    	index_modification = int(random.random() * len(palavra))
    	if (index_modification == 0):
    		palavra = chr(97 + int(26 * random.random())) + palavra[1:]
    	else:
    		palavra = palavra[:index_modification] + chr(97 + int(26 * random.random())) + palavra[index_modification+1:]
    	return palavra

    def mutaPop(self):
        crias = self.children()
        for i in range(len(crias)):
            if random.random() * 100 < self.propmut:
                crias[i] = self.mutacao(crias[i])
        return crias

    def darwin(self):
        score = 0
        epochs = 0
        while score < 100:
            self.gen = self.mutaPop()
            check = self.fitPop(self.gen)
            score = check[0][1]
            epochs += 1
            print(check[0])
            self.firstGen = False
        print("Number od generations: %d" % epochs)


teste = genalg("serounaosereisaquestao")
print(teste.darwin())
