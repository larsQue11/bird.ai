import numpy as np
from math import exp
from math import pow
import random

#create framework for a three layer Neural Network
class NeuralNetwork():

    def __init__(self,numInputs,numHiddenNeurons,numOutputs):
        self.numInputs = numInputs
        self.numHiddenNeurons = numHiddenNeurons
        self.numOutputs = numOutputs
        # self.inputLayerBias = np.reshape([np.random.random() for i in  range(self.numHiddenNeurons)],(self.numHiddenNeurons,1))
        # self.hiddenLayerBias = np.reshape([np.random.random() for i in  range(self.numOutputs)],(self.numOutputs,1))
        self.inputLayerBias = np.reshape([random.randint(1,99)/100 for i in  range(self.numHiddenNeurons)],(self.numHiddenNeurons,1))
        self.hiddenLayerBias = np.reshape([random.randint(1,99)/100 for i in  range(self.numOutputs)],(self.numOutputs,1))
        self.weightsInputToHidden = self.__initializeWeights(numInputs,numHiddenNeurons) #* np.sqrt(2/1)
        self.weightsHiddenToOutput = self.__initializeWeights(numHiddenNeurons,numOutputs) #* np.sqrt(2/1)
        # self.weightsInputToHidden = np.ones((2,3))
        # self.weightsHiddenToOutput = np.ones((1,3))

    def __initializeWeights(self,numOfSources,numOfDestinations):                  

        rows = numOfDestinations
        cols = numOfSources
        weights = []

        for row in range(rows):

            # currentRow = [np.random.random() for col in range(cols)]
            currentRow = [random.randint(1,99)/100 for col in range(cols)]
            weights.append(currentRow)

        #return a matrix with rows containing the input to each destination layer     
        return np.array(weights)


    '''
    Train the network through a feed-forward, backpropagation(stochastic gradient descent) algorithm:
    1: feed the data forward through the network
        A: inputs * weights + bias -> hidden layer
        B: compress data through sigmoid function
        C: hidden layer * weights + bias -> output
        D: smush data through sigmoid function
    2: make prediction from the output
    3: calculate the error between the actual classification and the prediction
    4: propagate the error backwards to adjust the weights accordingly
        A: calculate the gradients for the weights between each layer
        B: update weight matricies such that W = W + G
    '''
    def train(self,learningRate,trainingData):

        #trainingData must be a list where the first element is an array containing the inputs and
        #the second element is an array which pertains to the associated label or expected output        
        for trainer in trainingData:            
            #create a vector for the actual output
            targetVector = np.reshape(trainer[1],(self.numOutputs,1))

            #create an Nx1 vector with the input data            
            # inputVector = np.append(trainer[0],[self.inputLayerBias])
            inputVector = np.array(trainer[0])       
            inputVector = np.reshape(inputVector,(len(inputVector),1))
            
            #calculate hidden layer vector
            hiddenVectorIn = np.dot(self.weightsInputToHidden,inputVector)
            hiddenVectorIn = np.add(hiddenVectorIn,self.inputLayerBias)
            #run each value through sigmoid filter
            hiddenVectorOut = [self.__Sigmoid(i) for i in hiddenVectorIn]      
            hiddenVectorOut = np.reshape(hiddenVectorOut,(len(hiddenVectorOut),1))
                   
            #calculate output vector
            outputVectorIn = np.dot(self.weightsHiddenToOutput,hiddenVectorOut)
            outputVectorIn = np.add(outputVectorIn,self.hiddenLayerBias)
            outputVectorOut = [self.__Sigmoid(i) for i in outputVectorIn]            
            outputVectorOut = np.reshape(outputVectorOut,(len(outputVectorOut),1))     
            #calculate the error
            errorVectorOutput = np.subtract(targetVector,outputVectorOut)
            # errorVectorOutput = 0.5 * errorVectorOutput * errorVectorOutput
            

           
    def __Sigmoid(self,x):

        return 1 / (1 + exp(-x))

    def __dSigmoid(self,v):

        vector = np.ones((len(v),1))
        # dSigmoid = [self.__Sigmoid(i) for i in v]
        # dSigmoid = np.reshape(dSigmoid,(len(v),1))
        vector = np.subtract(vector,v)
        vector = v * vector

        return vector


    '''
    To make a prediction:
    1: create an input vector
    2: calculate the hidden layer vector as weights * inputs
    3: smush data through sigmoid
    4: calculate the outpt layer vector as weights * hidden
    5: smush data through sigmoid
    6: return the output vector
    '''
    def predict(self,data):

        inputVector = np.array(data)
        inputVector = np.reshape(inputVector,(self.numInputs,1))

        hiddenVector = np.dot(self.weightsInputToHidden,inputVector)
        hiddenVector = np.add(hiddenVector,self.inputLayerBias)
        hiddenVector = [self.__Sigmoid(i) for i in hiddenVector]
        hiddenVector = np.reshape(hiddenVector,(self.numHiddenNeurons,1))

        outputVector = np.dot(self.weightsHiddenToOutput,hiddenVector)
        outputVector = np.add(outputVector,self.hiddenLayerBias)
        outputVector = [self.__Sigmoid(i) for i in outputVector]
        outputVector = np.reshape(outputVector,(self.numOutputs,1))

        return outputVector

    # def getGenotype(self,mutationRate):

    #     # self.mutateWeights(mutationRate)
    #     rand = random.randint(1,100)
    #     if rand in range(1,int((mutationRate*100)+1)):
    #         dims = np.shape(self.inputLayerBias)
    #         inputLayerBias = np.copy(np.ndarray.flatten(self.inputLayerBias))
    #         # inputLayerBias = [pow(i,random.randint(1,8))%1 for i in inputLayerBias]
    #         # inputLayerBias = np.reshape(inputLayerBias,dims)
    #         print(inputLayerBias)
    #         print(self.inputLayerBias)

    #         dims = np.shape(self.weightsInputToHidden)
    #         weightsInputToHidden = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.weightsInputToHidden)]
    #         weightsInputToHidden = np.reshape(weightsInputToHidden,dims)

    #         dims = np.shape(self.hiddenLayerBias)
    #         hiddenLayerBias = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.hiddenLayerBias)]
    #         hiddenLayerBias = np.reshape(hiddenLayerBias,dims)

    #         dims = np.shape(self.weightsHiddenToOutput)
    #         weightsHiddenToOutput = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.weightsHiddenToOutput)]
    #         weightsHiddenToOutput = np.reshape(weightsHiddenToOutput,dims)

    #     return inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput

    def getGenotype(self):
        return np.copy(self.inputLayerBias), np.copy(self.weightsInputToHidden), np.copy(self.hiddenLayerBias), np.copy(self.weightsHiddenToOutput)

    def mutateWeights(self,mutationRate):

        '''
        rand = random.randint(1,100)
        if rand in range(1,int((mutationRate*100)+1)):
            dims = np.shape(self.inputLayerBias)
            inputLayerBias = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.inputLayerBias)]
            self.inputLayerBias = np.reshape(inputLayerBias,dims)

            dims = np.shape(self.weightsInputToHidden)
            weightsInputToHidden = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.weightsInputToHidden)]
            self.weightsInputToHidden = np.reshape(weightsInputToHidden,dims)

            dims = np.shape(self.hiddenLayerBias)
            hiddenLayerBias = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.hiddenLayerBias)]
            self.hiddenLayerBias = np.reshape(hiddenLayerBias,dims)

            dims = np.shape(self.weightsHiddenToOutput)
            weightsHiddenToOutput = [pow(i,random.randint(1,8))%1 for i in np.ndarray.flatten(self.weightsHiddenToOutput)]
            self.weightsHiddenToOutput = np.reshape(weightsHiddenToOutput,dims)
        '''

        
        dims = np.shape(self.inputLayerBias)
        inputLayerBias = np.ndarray.flatten(self.inputLayerBias)
        for weight in inputLayerBias:
            rand = random.randint(1,100)
            if rand in range(1,int((mutationRate*100)+1)):
                weight = self.decMutation(weight)
        self.inputLayerBias = np.reshape(inputLayerBias,dims)

        dims = np.shape(self.weightsInputToHidden)
        weightsInputToHidden = np.ndarray.flatten(self.weightsInputToHidden)
        for weight in weightsInputToHidden:
            rand = random.randint(1,100)
            if rand in range(1,int((mutationRate*100)+1)):
                weight = self.decMutation(weight)
        self.weightsInputToHidden = np.reshape(weightsInputToHidden,dims)

        dims = np.shape(self.hiddenLayerBias)
        hiddenLayerBias = np.ndarray.flatten(self.hiddenLayerBias)
        for weight in hiddenLayerBias:
            rand = random.randint(1,100)
            if rand in range(1,int((mutationRate*100)+1)):
                weight = self.decMutation(weight)
        self.hiddenLayerBias = np.reshape(hiddenLayerBias,dims)

        dims = np.shape(self.weightsHiddenToOutput)
        weightsHiddenToOutput = np.ndarray.flatten(self.weightsHiddenToOutput)
        for weight in weightsHiddenToOutput:
            rand = random.randint(1,100)
            if rand in range(1,int((mutationRate*100)+1)):
                weight = self.decMutation(weight)
        self.weightsHiddenToOutput = np.reshape(weightsHiddenToOutput,dims)
            

    def decMutation(self,value):

        intVal = int(value*100) + random.randint(-1,1)
        
        return intVal % 100

    def bitMutation(self,value):

        binVal = bin(int(value*100))
        if len(binVal) != 9:
            addZeros = 9 - len(binVal)
            binVal = binVal[:2] + ('0' * addZeros) + binVal[2:]

        indexOfMutation = random.randint(2,8)
        if binVal[indexOfMutation] == '1':
            binVal = binVal[:indexOfMutation] + '0' + binVal[indexOfMutation:]
        else:
            binVal = binVal[:indexOfMutation] + '1' + binVal[indexOfMutation:]

        return int(binVal,2)/100