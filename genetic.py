import json
import sys
import time
import numpy as np
from random import uniform


class ProblemDescriptor():
    """Interface"""

    def getDefinedSeeds(self):
        pass

    def getMutationLimits(self):
        pass

    def calculateScore(self, candidate):
        pass

    def geneMeaning(self):
        pass




def getAttribute(position):
    if len(sys.argv) > position:
        return sys.argv[position]
    else:
        raise ValueError("argument expected in position " + str(position))

def getConfFileName():
    return getAttribute(1)

def getParameterFromConfFile(parameter):
    f = open(getConfFileName(),)
    confJson = json.load(f)
    return confJson[parameter]

def getNumberOfEpochs():
    return int(getParameterFromConfFile('numberOfEpochs'))

def getPopulationNumber():
    return int(getParameterFromConfFile('populationNumber'))

def getRandomsRate():
    return float(getParameterFromConfFile('randomsRate'))/100.0

def getChampionsRate():
    return float(getParameterFromConfFile('championsRate'))/100.0

def getTimeout():
    return float(getParameterFromConfFile('timeout'))

def getGoal():
    return float(getParameterFromConfFile('goal'))

class Clock(object):
    def __init__(self):
        self.startTime = time.time()
        self.timeout = getTimeout()

    def isTimeout(self):
        self.elapsedTime = time.time() - self.startTime
        if self.elapsedTime > getTimeout():
            return True
        else:
            return False
    def getElapsedTime(self):
        return self.elapsedTime

class Population(object):
    """docstring for Population"""
    
    def __init__(self, problemDescriptor):
        self.problemDescriptor = problemDescriptor
        self.population = problemDescriptor.getDefinedSeeds()
        self.epoch = 0
        self.clock = Clock()
        self.bestScore = 0

    def evolve(self):
        self.newPopulation = []
        self.appendChampions()
        self.appendRandoms()
        self.appendChildren()
        self.population = self.newPopulation
        self.epoch+=1
        return



    def appendChildren(self):
        childrenNumber = getPopulationNumber() - len(self.newPopulation)

        individualA = self.population[self.randomIndividualIndex()]
        individualB = self.population[self.randomIndividualIndex()]

        for _ in range(childrenNumber):
            self.newPopulation.append(self.mateIndividuals(individualA, individualB))

    def randomIndividualIndex(self):
        return self.randomIndex(len(self.population))

    def mateIndividuals(self, individualA, individualB):
        newIndividual = []
        couple = [individualA, individualB]

        for geneIndex in range(len(individualA)):
            gene = couple[self.randomPartnerIndex()][geneIndex]
            newIndividual.append(gene)
            
        self.mutateGene(self.randomGeneToMutate(),newIndividual)
        return newIndividual

    def randomIndex(self, size):
        return int(uniform(0,size-1))

    def randomGeneToMutate(self):
        return self.randomIndex(3)

    def randomPartnerIndex(self):
        return self.randomIndex(1)

    def appendChampions(self):
        championsRate = getChampionsRate()
        populationNumber = getPopulationNumber()
        numberOfChampions = int(championsRate*populationNumber)
        if numberOfChampions < 1:
            return

        self.appendFittest(numberOfChampions)


    def appendRandoms(self):
        randomsRate = getRandomsRate()
        populationNumber = getPopulationNumber()
        numberOfRandoms = int(randomsRate*populationNumber)
        if numberOfRandoms < 1:
            return

        for _ in range(numberOfRandoms):
            self.newPopulation.append(self.generateRandomIndividual())


    def mutateGene(self,geneIndex,individual):
        mutationLimits = self.problemDescriptor.getMutationLimits()

        if individual[geneIndex] == 0:
            inferiorLimits = mutationLimits[0]
            superiorLimits = mutationLimits[1]
        else:
            inferiorLimits = self.multiplyListByFactor(individual,0.5)
            superiorLimits = self.multiplyListByFactor(individual,1.5)

        if inferiorLimits < mutationLimits[0]:
            inferiorLimits = mutationLimits[0]
        if superiorLimits > mutationLimits[1]:
            superiorLimits = mutationLimits[1]

        individual[geneIndex] = int(uniform(inferiorLimits[geneIndex], superiorLimits[geneIndex]))
        
    def multiplyListByFactor(self, list, factor):
        return (np.array(list)*factor).tolist()
        
    def generateRandomIndividual(self):
        mutationLimits = self.problemDescriptor.getMutationLimits()
        individualSize = len(mutationLimits[0])

        individual = np.zeros(individualSize).tolist()
        for index in range(individualSize):
            self.mutateGene(index, individual)

        return individual


    def appendFittest(self, number):
        scores = list(map(self.problemDescriptor.calculateScore, self.population))
        try:
            sortedPopulation = [x for _, x in sorted(zip(scores, self.population))]
        except Exception as e:
            print(scores)
            print(self.population)
            exit()

        if len(scores) > 0:
            self.bestScore = sorted(scores)[-1]
            self.bestIndividual = sortedPopulation[-1]
            
        for individual in sortedPopulation[-number:]:
            self.newPopulation.append(individual)



    def isBelowCriteria(self):

        if self.epoch > getNumberOfEpochs():
            print("epoch limit")
            return False
        if self.clock.isTimeout():
            print("timeout")
            return False


        goal = getGoal()
        for individual in self.population:
            individualScore = self.problemDescriptor.calculateScore(individual)
            if individualScore > goal:
                self.bestScore = individualScore
                self.bestIndividual = individual

                print("goal achieved")
                return False

        return True

    def report(self):
        print("numberOfEpochs: " + str(self.epoch))
        print("elapsedTime: " + str(self.clock.getElapsedTime()))
        print("bestScore: " + str(self.bestScore))
        print("population:" + str(len(self.population)))
        print("geneMeaning: " + self.problemDescriptor.geneMeaning())
        print("bestIndividual: " + str(self.bestIndividual))

def start(problemDescriptor):
    
    population = Population(problemDescriptor)

    while(population.isBelowCriteria()):
        population.evolve()
        print(population.bestScore)

    population.report()


if __name__ == "__main__":
    #start()
    pass