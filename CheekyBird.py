import pygame
import time
import random
import NeuralNetwork as nn
import Bird
import numpy as np


'''
Dimensions of game objects:
Background: 864x512
Ground: 864x112
Bird: 
Coin: 22x27
Column: 
'''

WindowWidth = 864
WindowHeight = 512

# BirdWingUpSprite = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bird1.png")))

BackgroundImage = pygame.image.load('./images/background.png')
pygame.font.init()
Font = pygame.font.Font("./LuckiestGuy.ttf", 30)


class Pipe:
    PipeSprite = pygame.image.load('./images/pipe.png')
    Gap = 100
    Velocity = 5

    def __init__(self,x):
        self.posX = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.TopPipe = pygame.transform.flip(self.PipeSprite, False, True)
        self.BottomPipe = self.PipeSprite
        self.pipePassed = False
        self.setHeight()
        self.centerOfGap = (self.bottom - self.top) / 2


    def setHeight(self):

        self.height = random.randrange(50,WindowHeight-112-50-self.Gap) #112 is the height of the base, 50 is the minimum y position
        self.top = self.height - self.TopPipe.get_height()
        self.bottom = self.height + self.Gap


    def move(self):

        self.posX = self.posX - self.Velocity

    def draw(self,window):

        window.blit(self.TopPipe,(self.posX,self.top))
        window.blit(self.BottomPipe,(self.posX,self.bottom))

    def collide(self,bird):

        birdMask = bird.getMask()
        topPipeMask = pygame.mask.from_surface(self.TopPipe)
        bottomPipeMask = pygame.mask.from_surface(self.BottomPipe)

        topOffset = (self.posX - bird.posX, self.top - round(bird.posY))
        bottomOffset = (self.posX - bird.posX, self.bottom - round(bird.posY))

        bottomCollisionPoint = birdMask.overlap(bottomPipeMask,bottomOffset)
        topCollisionPoint = birdMask.overlap(topPipeMask,topOffset)

        if topCollisionPoint or bottomCollisionPoint:
            return True
        else:
            return False


class Base():
    GroundSprite = pygame.image.load('./images/ground.png')
    Velocity = 5
    Width = GroundSprite.get_width()

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Width

    def move(self):
        self.x1 = self.x1 - self.Velocity
        self.x2 = self.x2 - self.Velocity

        if self.x1 + self.Width < 0:
            self.x1 = self.x2 + self.Width

        if self.x2 + self.Width < 0:
            self.x2 = self.x1 + self.Width

    def draw(self,window):
        window.blit(self.GroundSprite,(self.x1,self.y))
        window.blit(self.GroundSprite,(self.x2,self.y))

    def collide(self,bird):

        birdMask = bird.getMask()
        groundMask1 = pygame.mask.from_surface(self.GroundSprite)
        groundMask2 = pygame.mask.from_surface(self.GroundSprite)

        offset1 = (self.x1 - bird.posX, 400 - round(bird.posY))
        offset2 = (self.x2 - bird.posX, 400 - round(bird.posY))

        base1Collision = birdMask.overlap(groundMask1,offset1)
        base2Collision = birdMask.overlap(groundMask2,offset2)
    

        if base1Collision or base2Collision:
            return True
        else:
            return False


def drawWindow(window,birds,pipes,base,score):
    window.blit(BackgroundImage,(0,0))

    for pipe in pipes:
        pipe.draw(window)

    text = Font.render(f"Score: {score}",True,(255,255,255))
    window.blit(text,(10,10))
    base.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def generatePipe(distance):

    distance = distance + random.randint(250,400)
    return Pipe(distance)

# def crossover()


def generation():

    window = pygame.display.set_mode((WindowWidth,WindowHeight))
    gameClock = pygame.time.Clock()

    populationSize = 100 #number of birds to start with
    numberOfDeadBirds = 0
    numberOfParents = 2
    deadBirdThreshold = populationSize - numberOfParents
    birds = [Bird.Bird() for i in range(populationSize)]
    base = Base(400)
    gameScore = 0
    pipesPassed = 0
    run = True
    gameObjects = [Pipe(400 * i) for i in range(1,20)]
    nextObject = gameObjects[pipesPassed]
    newGeneration = True
    while run:
        #TODO: change dynamically with key press
        # if numberOfDeadBirds == 0:
        #     gameClock.tick(30)
        # elif numberOfDeadBirds > 50:
        # gameClock.tick(40)

        for event in pygame.event.get():
            gameClock.tick(30)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
      
        #begin moving the objects in the game
        for obj in gameObjects:
            obj.move()

        #begin moving the base
        base.move()
        # for bird in birds:
        #     bird.move()
        if newGeneration:
            deadBirds = []
            numberOfDeadBirds = 0
            gameScore = 0
            pipesPassed = 0
            gameObjects = [Pipe(100 + (i*400)) for i in range(1,20)]
            nextObject = gameObjects[pipesPassed]
            drawWindow(window,birds,gameObjects,base,gameScore)
            newGeneration = False
        
        
        for bird in birds:
            bird.fitness = bird.fitness + 0.1
            currentVerticalPosition = bird.posY
            distanceToNextPole = nextObject.posX - bird.posX
            centroidOfUpcomingGap = nextObject.centerOfGap
            inputVector = [currentVerticalPosition,distanceToNextPole,centroidOfUpcomingGap]
            # bird.move(inputVector)

            #check if the bird collides with the pipe, bird dies if True
            if nextObject.collide(bird):
                print("Pipe collision")
                bird.fitness = bird.fitness + gameScore
                bird.died = True
                numberOfDeadBirds = numberOfDeadBirds + 1                

            # check for base collision, bird dies if true
            if bird.posY >= 400:
                print("Base collision")
                bird.fitness = bird.fitness + gameScore
                bird.died = True
                numberOfDeadBirds = numberOfDeadBirds + 1
            
            # currentVerticalPosition = bird.posY
            # distanceToNextPole = nextObject.posX - bird.posX
            # centroidOfUpcomingGap = nextObject.centerOfGap
            # inputVector = [currentVerticalPosition,distanceToNextPole,centroidOfUpcomingGap]
            # bird.makeDecision(inputVector)


        deadBirds = deadBirds + [bird for bird in birds if bird.died]
        birds = [bird for bird in birds if not bird.died]

        if len(deadBirds) == populationSize:
            deadBirds.sort(key=lambda x: x.fitness, reverse=True)
            birds = []
            for bird in deadBirds[:5]:
                inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput = bird.birdBrain.getGenotype()
                goodBird = Bird.Bird()
                goodBird.birdBrain.inputLayerBias = inputLayerBias
                goodBird.birdBrain.weightsInputToHidden = weightsInputToHidden
                goodBird.birdBrain.hiddenLayerBias = hiddenLayerBias
                goodBird.birdBrain.weightsHiddenToOutput = weightsHiddenToOutput
                birds.append(goodBird)
            birds = birds + birds[:]
            for bird in birds[5:]:
                bird.birdBrain.mutateWeights(0.8)
            birds = birds + [Bird.Bird() for i in range(populationSize-len(birds))]
            newGeneration = True
        else:
            #TODO: check if next object is a pipe or coin
            if nextObject.posX < birds[0].posX:
                gameScore = gameScore + 1
                pipesPassed = pipesPassed + 1
                nextObject = gameObjects[pipesPassed]
                gameObjects.append(generatePipe(gameObjects[len(gameObjects)-1].posX))
            drawWindow(window,birds,gameObjects,base,gameScore)


        '''
        bestPerformers = []
        if numberOfDeadBirds < deadBirdThreshold:
            birds = [bird for bird in birds if not bird.died]
            drawWindow(window,birds,gameObjects,base,gameScore)
        elif numberOfDeadBirds > deadBirdThreshold and numberOfDeadBirds < populationSize:
            for bird in birds:
                if bird.died:
                    bestPerformers.append(bird)
            birds = [bird for bird in birds if not bird.died]
            drawWindow(window,birds,gameObjects,base,gameScore)
        elif numberOfDeadBirds == populationSize:
            #TODO: evolution stuff
            birds = []
            if len(bestPerformers) != 0:
                
                for bird in bestPerformers:
                    inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput = bird.birdBrain.getGenotype(0.2)
                    goodBird = Bird.Bird()
                    goodBird.birdBrain.inputLayerBias = inputLayerBias
                    goodBird.birdBrain.weightsInputToHidden = weightsInputToHidden
                    goodBird.birdBrain.hiddenLayerBias = hiddenLayerBias
                    goodBird.birdBrain.weightsHiddenToOutput = weightsHiddenToOutput
                    birds.append(bird)
            else:
                #do something to force change in the data if all birds die together            
                birds = [Bird.Bird() for i in range(populationSize//2)]
                for bird in birds:
                    bird.birdBrain.mutateWeights(0.8)
            
            birds = birds + [Bird.Bird() for i in range(populationSize-len(birds))]
            numberOfDeadBirds = 0
            gameScore = 0
            pipesPassed = 0
            gameObjects = [Pipe(600 + (i*400)) for i in range(1,20)]
            nextObject = gameObjects[pipesPassed]
            drawWindow(window,birds,gameObjects,base,gameScore)
            '''
            

        #TODO: remove old objects to decrease memory usage
        # if gameObjects[0].posX + gameObjects[0].TopPipe.get_width() < 0: #is pipe off screen?
        #     gameObjects.pop(0)
            

        
        
        #base collision
        # if bird.posY + bird.currentSprite.get_height() >= 400:
        #     print("Base collision")
        # if base.collide(bird):
        #     print("base collision")
    #end of game exits here
    

if __name__ == "__main__":
    generation()