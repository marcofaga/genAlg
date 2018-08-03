'''
Construindo um algoritmo genético
A ideia aqui é tentar descobrir qual é a senha escondida
Tirado de: https://blog.sicara.com/getting-started-genetic-algorithms-python-tutorial-81ffa1dd72f9
'''

# A função fitness define o score da palavra escolhida

def fitness (password, test_word):

	if (len(test_word) != len(password)):
		print("taille incompatible")
		return
	else:
		score = 0
		i = 0
		while (i < len(password)):
			if (password[i] == test_word[i]):
				score+=1
			i+=1
		return score * 100 / len(password)

'''
Características dos indivíduos:
os indivíduos serão as palavras de mesmo tamanho da palavra
a ser decifrada. Os alelos serão as letras que compõem esta palavra.
palavra = banana
alelo = b, a, n...

Criando a primeira população:
A primeira população não deve ser a melhor, mas aquela que corresponde à maior
variabilidade possível. Assim começaremos com palavras que contém sequências
aleatórias de letras.

'''

import random

# define uma sequência de caracteres aleatória
def generateAWord (length):
	i = 0
	result = ""
	while i < length:
		letter = chr(97 + int(26 * random.random()))
		result += letter
		i +=1
	return result

#palavra = generateAWord(10)
#print(palavra)

def generateFirstPopulation(sizePopulation, password):
	population = []
	i = 0
	while i < sizePopulation:
		population.append(generateAWord(len(password)))
		i+=1
	return population

password = "pipoca"
firstopop = generateFirstPopulation(100, password)
#print(firstopop)

'''
Evolução:
A partir da primeira população, começamos o processo de evolução.
O objetivo do algoritmo aqui é selecionar as melhores soluções da geração
anterior.  o perigo aqui é que se você selecionar apenas as melhores soluções
você poderá chegar a um mínimo local, e não à melhor solução possível. Por isso
você não deve simplesmente jogar fora as piores soluções. Elas devem ser
incorporadas.

A solução é selecionar de um lado as N melhores espécimes e de outrao selecionar
M indivíduos aleatórios sem distinção de qual score é melhor.

'''

# acerta o fitness de cada população inicial e hierarquiza.
import operator

def computePerfPopulation(population, password):
	populationPerf = {}
	for individual in population:
		populationPerf[individual] = fitness(password, individual)
	return sorted(populationPerf.items(), key = operator.itemgetter(1), reverse=True)

fitnesspop = computePerfPopulation(firstopop, password)
#print(fitnesspop)

#faz a seleção das N espécimes que sobreviveram e das M aleatórias que não.
def selectFromPopulation(populationSorted, best_sample, lucky_few):
	nextGeneration = []
	for i in range(best_sample):
		nextGeneration.append(populationSorted[i][0])
	for i in range(lucky_few):
		nextGeneration.append(random.choice(populationSorted)[0])
	random.shuffle(nextGeneration)
	return nextGeneration

breeders = selectFromPopulation(fitnesspop, 50, 50)
#print(nextgen)

'''
Acasalamento:
Agora é hora de cruzar os genes vencedores com os aleatórios perdedores.
Ou seja, é preciso fazer um cruzamento das palavras, de modo a que seus filhos
tenham genes misturados do pai e da mão. A maneira de fazer isso é fazendo com
que o filho tenha, para cada letra sua, uma letra aleatória do pai ou da mãe.
Ex: do cruzamento entre abc e ghi, o filho poderia ser agh, bha, cia e etc...

Importante controlar o número de filhos para que cada geração tenha a mesma
população da anterior.
'''

def createChild(individual1, individual2):
	child = ""
	for i in range(len(individual1)):
		if (int(100 * random.random()) < 50):
			child += individual1[i]
		else:
			child += individual2[i]
	return child

def createChildren(breeders, number_of_child):
	nextPopulation = []
	for i in range(int(len(breeders)/2)):
		for j in range(number_of_child):
			nextPopulation.append(createChild(breeders[i], breeders[len(breeders) -1 -i]))
	return nextPopulation

nextpop = createChildren(breeders, len(firstopop))
#print(nextpop)

'''
Mutação:
É a última etapa do algoritmo. Após o acasalamento, cada indivíduo deve ter uma
pequena probabilidade de terem seus DNAs mudando um pouco. Essa operação é
importante para prevenir que o algoritmo fique bloqueado em um mínimo local.
Sempre buscamos o melhor resultado, ou seja, o mínimo global.

Para isso existem algumas técnicas, como a escolha da taxa de mutação de cada
geração.

'''

def mutateWord(word):
	index_modification = int(random.random() * len(word))
	if (index_modification == 0):
		word = chr(97 + int(26 * random.random())) + word[1:]
	else:
		word = word[:index_modification] + chr(97 + int(26 * random.random())) + word[index_modification+1:]
	return word

def mutatePopulation(population, chance_of_mutation):
	for i in range(len(population)):
		if random.random() * 100 < chance_of_mutation:
			population[i] = mutateWord(population[i])
	return population

popmutation = mutatePopulation(nextpop, 0.1)
print(popmutation)


#Ok, vamos implementar no arquivo seguinte uma classe de algoritmo genético
