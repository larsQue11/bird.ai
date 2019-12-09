import numpy as np

class Learning():

    def __init__(self):
        '''
        Define the Table and initialize all values to zero
        The state of the agent is a 2D state space: the horizontal and vertical distances
        between the bird and the centroid of the upcoming obstacle's gap
            -rows: horizontal distance
            -cols: vertical distance

        The "depth" of the matrix is used to predict the action associated with the highest reward.
        The structure of a 3D Numpy array is: (rows,cols,depth)

        Because we know the maximum/minimum positions for both the bird and the objects,
        we can reduce the state space:
            -Bird is always at x = 150, y can range from 0 to 400
            -The next pipe will be at an x position between 400 and 150 (Bird's position),
            the center of the gap will be will be in a range of 125 to 275 vertically.
            -This reduces to a square 2D matrix of 250x499
                -499 is needed to describe when the bird is above the gap and vice versa
                    0-249: deltaY > 0 -> bird above gap
                    250: deltaY = 0 -> bird and gap on same level
                    251-499: deltaY < 0 -> bird below gap

        Example: Bird is at position (150,200) and Gap at (275,250)
        The differnce vector will be (125,50)
        **Note that the state space is not the current position of the bird and the gap, but the
        distances between the two.

        The goal of this algorithm is that all possible states can be defined by the state space.
        At any time during the game, the algorithm will process the current state space and return
        the appropriate action based on the value that's stored in the depth layer of the matrix.


        '''
        #initialize the Q matrix where the 2D array represents the state space and the 2 value 
        #vector is the Q value associated with the actions jump and don't jump, respectively

        self.QTable = np.ndarray((400,499,2))
        for x in range(400):
            self.QTable[x] = 0
        self.learningRate = 0.4 #0.4
        self.discount = 0.95 #0.8

        self.updateInfo = None


    def exploit(self,deltaX,deltaY):

        print("Exploit")
        qVector = self.QTable[deltaX][deltaY]

        if qVector[1] > qVector[0]:
            # print("JUMP!")
            return 1
        else:
            return 0

    #use state after action made?
    def explore(self,deltaX,deltaY):
        print("Explore")
        action = self.exploit(deltaX,deltaY)
        # action = np.random.randint(2)
        # action = 0
        self.updateInfo = [deltaX,deltaY,action]
        
        return action


    def updateFromExploration(self,deltaX,deltaY,reward):
        
        oldX = self.updateInfo[0]
        oldY = self.updateInfo[1]
        actionTaken = self.updateInfo[2]

        nextState = self.QTable[deltaX][deltaY] #the current state, the result of action taken in previous step
        oldValue = (1-self.learningRate) * self.QTable[oldX][oldY][actionTaken] #Q value associated with action taken
        learnedValue = reward + (self.discount * np.max(nextState))
        # print(f"Location: {self.QTable[self.updateInfo[0]][self.updateInfo[1]][self.updateInfo[2]]}")
        # self.QTable[self.updateInfo[0]][self.updateInfo[1]][self.updateInfo[2]] = oldValue + (self.learningRate * learnedValue)
        newQ = oldValue + (self.learningRate * learnedValue)
        self.QTable.itemset((oldX,oldY,actionTaken),newQ)
        # print(f"Q' = {newQ}")
        # print(f"New Q vector: {self.QTable[oldX][oldY]}")

        # print(f"Value: {self.QTable[self.updateInfo[0]][self.updateInfo[1]][self.updateInfo[2]]}")

        #previously comma-separated
        self.updateInfo = None
        # print(self.updateInfo[2])
        # print(oldValue + (self.learningRate * learnedValue))
        


    def loadState(self):

        self.QTable = np.load('./QTable.npy')


    def saveState(self):

        np.save('./QTable',self.QTable)



# test = Learning()
# print(len(test.QTable[0][1])) #2
# print(len(test.QTable[0])) #499
# print(len(test.QTable)) #400
# print(test.QTable[1,1])
# test.explore(250,250)
# print(test.updateInfo)
# test.updateFromExploration(251,251,100)
# print(test.QTable[250,250])
# print(test.updateInfo)