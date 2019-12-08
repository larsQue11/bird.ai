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
        self.learningRate = 0.4
        self.discount = 0.8

        self.updateInfo = None


    def exploit(self,deltaX,deltaY):

        
        qVector = self.QTable[deltaX,deltaY]

        if qVector[1] > qVector[0]:
            return 1
        else:
            return 0

    #use state after action made?
    def explore(self,deltaX,deltaY):

        action = self.exploit(deltaX,deltaY)
        self.updateInfo = (deltaX,deltaY,action)
        
        return action


    def updateFromExploration(self,deltaX,deltaY,reward):

        nextState = self.QTable[deltaX,deltaY]
        oldValue = (1-self.learningRate) * self.QTable[self.updateInfo[0],self.updateInfo[1],self.updateInfo[2]]
        learnedValue = reward + (self.discount * np.max(nextState))
        self.QTable[self.updateInfo[0],self.updateInfo[1],self.updateInfo[2]] = oldValue + (self.learningRate * learnedValue)
        
        # print(self.updateInfo[2])
        # print(oldValue + (self.learningRate * learnedValue))
        # print(self.QTable[self.updateInfo[0],self.updateInfo[1],self.updateInfo[2]])


    def loadState(self):

        self.QTable = np.load('./QTable.npy')


    def saveState(self):

        np.save('./QTable',self.QTable)


