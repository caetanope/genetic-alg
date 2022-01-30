'''problema criação de gado

numero cabeças
area de criação
quantidade de ração
idade de abate
quantidade de suplementação

investimento 1 milao e 5 anos
1000 reais por terneiro(100kgs)
1 reais o metro quadrado pasto
15 reais o kg do animal vivo
4 reais o kg da ração
1 kg de ração ~> 0.3 kg de animal

'''

import numpy as np
import genetic

__SUPLEMENT_PRICE__ = 3
__TOTAL_TIME__ = 20
__LAND_PRICE__ = 4
__INITIAL_WEIGHT__ = 100
__LIVE_STOCK_PRICE__ = 15
__NEW_ANIMAL_COST__ = __LIVE_STOCK_PRICE__ * __INITIAL_WEIGHT__
__INITIAL_CASH__ = 1000000


def ln(value):
	return float(np.log(value))

def calculateWeight(initialWeight,ageOfSlaughter,space,suplement):
	return initialWeight + (ln(ageOfSlaughter)*1.5 + 1)*((ln(space/500)+1)*10 + suplement**(1/2)*3)+18

def calculateSuplementCost(numberOfAnimals, amountOfSuplement, price, totalTime):
	return numberOfAnimals * amountOfSuplement * price * totalTime

def calculateLandCost(numberOfAnimals, space, price, totalTime):
	return numberOfAnimals * space * price * totalTime

def calculateStockValue(weight, numberOfAnimals, price, ageOfSlaughter, totalTime):
	return (weight * numberOfAnimals * price) * (totalTime / ageOfSlaughter)

def calculateAnimalsCost(numberOfAnimals, price, ageOfSlaughter, totalTime):
	return (numberOfAnimals * price) * (totalTime / ageOfSlaughter)

def calculateNetWorth(numberOfAnimals, suplement, ageOfSlaughter, space):
	weight = calculateWeight(__INITIAL_WEIGHT__, ageOfSlaughter, space, suplement)
	return float( __INITIAL_CASH__ 
			- calculateSuplementCost(numberOfAnimals, suplement, __SUPLEMENT_PRICE__, __TOTAL_TIME__)	
			- calculateLandCost(numberOfAnimals, space, __LAND_PRICE__, __TOTAL_TIME__)
			- calculateAnimalsCost(numberOfAnimals, __NEW_ANIMAL_COST__, ageOfSlaughter, __TOTAL_TIME__)
			+ calculateStockValue(weight, numberOfAnimals, __LIVE_STOCK_PRICE__, ageOfSlaughter, __TOTAL_TIME__) )

def test():
	print(calculateWeight(100,1,1000,0))
	print(calculateWeight(100,2,1000,0))
	print(calculateWeight(100,3,1000,0))
	print(calculateWeight(100,4,1000,0))
	print(calculateWeight(100,5,1000,0))
	
	print(calculateWeight(100,1,5000,0))
	
	print(calculateWeight(100,5,1000,100))
	
	print(calculateNetWorth(100, 10, 1, 1000))


class Farm(genetic.ProblemDescriptor):
	def geneMeaning(self):
		return "numberOfAnimals, suplementPerYear, ageOfSlaughter, space"

	def getDefinedSeeds(self):
		return [[100, 10, 1, 1000]]

	def getMutationLimits(self):
		return [[1,0,1,10],
				[1000, 1000, __TOTAL_TIME__, 10000]]

	def calculateScore(self, candidate):
		return calculateNetWorth(candidate[0], candidate[1], candidate[2], candidate[3])

if __name__ == "__main__":
	genetic.start(Farm())
	#test()