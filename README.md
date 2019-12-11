Instructions for use:

Add Numpy and Pygame modules to your Python3
Run the CheekyBird.py file

Library files:
* NeuralNetwork.py: a 3-layer artificial neural network
* GeneticAlgorithm.py: the genetic algorithm
* Bird.py: the agent

To adjust the ANN architecture, go to the Bird.py file and find the "birdBrain" attribute defined 
in the initialization function. Initializing the NN takes three parameters: #input neurons, #hidden neurons, #output neurons.
Passing the desired number of neurons into the birdBrain gives you the respective configuration.

The population size created each generation is handed by the population variable in the driver file.
