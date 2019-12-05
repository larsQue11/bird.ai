from math import pow
import random
import NewBird as Bird
import NeuralNetwork as nn
import numpy as np

class GenerateNewPopulation():

    def __init__(self,populationSize,oldPopulation=None):
        self.populationSize = populationSize
        if not oldPopulation:
            #create a new generation from scratch
            self.nextGeneration = [Bird.Bird() for bird in range(populationSize)]

        else:
            self.__normalizeFitness(oldPopulation)
            #select new birds based on fitness
            self.nextGeneration = [self.__naturalSelection(oldPopulation) for i in range(populationSize)]
            
            for bird in self.nextGeneration:
                bird.birdBrain.inputLayerBias = self.__mutate(bird.birdBrain.inputLayerBias)
                bird.birdBrain.weightsInputToHidden = self.__mutate(bird.birdBrain.weightsInputToHidden)
                bird.birdBrain.hiddenLayerBias = self.__mutate(bird.birdBrain.hiddenLayerBias)
                bird.birdBrain.weightsHiddenToOutput = self.__mutate(bird.birdBrain.weightsHiddenToOutput)


    def __naturalSelection(self,oldPopulation):

        selectionProbability = random.random()
        for bird in oldPopulation:
            if bird.positionY != 0:
                selectionProbability = selectionProbability - bird.fitness
                if selectionProbability < 0:
                    inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput = bird.birdBrain.getGenotype()
                    goodBird = Bird.Bird()
                    goodBird.birdBrain.inputLayerBias = inputLayerBias[:]
                    goodBird.birdBrain.weightsInputToHidden = weightsInputToHidden[:]
                    goodBird.birdBrain.hiddenLayerBias = hiddenLayerBias[:]
                    goodBird.birdBrain.weightsHiddenToOutput = weightsHiddenToOutput[:]
                    return goodBird


    def __mutate(self,matrix):

        dims = np.shape(matrix)
        matrix = np.ndarray.flatten(matrix)
        mutationRate = 0.2
        for value in matrix:
            if random.random() < mutationRate:
                value = (value + random.gauss(0.5,0.25)*5) % 1
            else:
                pass
        
        return np.reshape(matrix,dims)


    def __normalizeFitness(self,oldPopulation):
        
        populationFitness = 0
        for bird in oldPopulation:
            bird.fitness = pow(bird.fitness,2)
            populationFitness = populationFitness + bird.fitness

        for bird in oldPopulation:
            bird.fitness = bird.fitness / populationFitness
        
