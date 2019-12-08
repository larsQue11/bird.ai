import pygame
import time
import random
import NeuralNetwork as nn
import Bird as Bird
import GeneticAlgorithm as ga
import numpy as np

'''
TODO:
-handle bird death on collision
-what to do when all birds die
-how to start new generation
    -set generation to False
-start new pipe flow
-bird ai
-generational evolution

'''

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
BackgroundImage = pygame.image.load('./images/background.png')
pygame.font.init()
Font = pygame.font.Font("./LuckiestGuy.ttf", 26)


class Pipe:
    PipeSprite = pygame.image.load('./images/pipe.png')
    Gap = 150
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

        topOffset = (self.posX - bird.positionX, self.top - round(bird.positionY))
        bottomOffset = (self.posX - bird.positionX, self.bottom - round(bird.positionY))

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

    def __init__(self):
        self.y = 400
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


def drawWindow(window,birds,pipes,base,text):
    window.blit(BackgroundImage,(0,0))

    for pipe in pipes:
        pipe.draw(window)

    text = Font.render(f"Generation: {text[0]} High Score: {text[1]} Current Score: {text[2]}",True,(255,255,255))
    # text = [Font.render(f"Generation: {text[0]}",True,(255,255,255)), Font.render(f"High Score: {text[1]}",True,(255,255,255)), Font.render(f"Current Score: {text[2]}",True,(255,255,255))]
    window.blit(text,(10,10))
    base.draw(window)
    
    # bird.draw(window)
    for bird in birds:
        bird.draw(window)
    pygame.display.update()


def generatePipe(distance):

    distance = distance + random.randint(250,400)
    return Pipe(distance)


def birdEvolution():
    
    gameClock = pygame.time.Clock()
    stillLearning = True
    currentGeneration = 0
    highScore = 0
    populationSize = 200
    birds = ga.GenerateNewPopulation(200).nextGeneration
    while stillLearning:

        #Following represents a single generation of evolution
        window = pygame.display.set_mode((WindowWidth,WindowHeight))
        base = Base()
        gameScore = 0
        pipesPassed = 0
        gameObjects = [Pipe((400 * i)) for i in range(1,20)]
        nextObject = gameObjects[pipesPassed]
        generation = True
        
        # bird = Bird.Bird()
        
        deadBirds = []
        while generation:
            
            #time control
            # gameClock.tick(30)
            # pygame.time.delay(30)
            drawWindow(window,birds,gameObjects,base,[currentGeneration,highScore,gameScore])
            for event in pygame.event.get():
                # gameClock.tick(30)
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        run = False
                    elif event.key == pygame.K_SPACE :
                        for bird in birds:
                            bird.jumpKey()
                elif event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            for obj in gameObjects:
                obj.move()

            base.move()
            for bird in birds:
                bird.fitness = bird.fitness + 0.1
                currentVerticalPosition = (400 - bird.positionY) / 400
                currentVelocity = bird.velocityY / 16
                distanceToNextPole = (nextObject.posX - bird.positionX) / (WindowWidth)
                centroidOfUpcomingGap = (bird.positionY - nextObject.centerOfGap)/ 400                
                inputVector = [currentVerticalPosition,currentVelocity,distanceToNextPole,centroidOfUpcomingGap]
                bird.jump(inputVector)
                bird.update()

                if nextObject.collide(bird):
                    print("Pipe collision")
                    bird.died = True
                    bird.fitness = bird.fitness + (gameScore*10)
                                

                # check for base collision, bird dies if true
                if bird.positionY >= 400:
                    print("Base collision")
                    bird.died = True
                    bird.fitness = bird.fitness + (gameScore*10)
                
            if nextObject.posX < birds[0].positionX:
                gameScore = gameScore + 1
                pipesPassed = pipesPassed + 1
                nextObject = gameObjects[pipesPassed]
                gameObjects.append(generatePipe(gameObjects[len(gameObjects)-1].posX))
                for bird in birds:
                    if not bird.died:
                        bird.fitness = bird.fitness + 10

            deadBirds = deadBirds + [bird for bird in birds if bird.died]
            birds = [bird for bird in birds if not bird.died]

            if len(deadBirds) == populationSize:
                generation = False
                
                '''
                for bird in deadBirds[:5]:
                    inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput = bird.birdBrain.getGenotype()
                    goodBird = Bird.Bird()
                    goodBird.birdBrain.inputLayerBias = inputLayerBias[:]
                    goodBird.birdBrain.weightsInputToHidden = weightsInputToHidden[:]
                    goodBird.birdBrain.hiddenLayerBias = hiddenLayerBias[:]
                    goodBird.birdBrain.weightsHiddenToOutput = weightsHiddenToOutput[:]
                    birds.append(goodBird)
                    
                '''
                # birds = birds + birds[:]
                # for bird in birds[5:]:
                #     bird.birdBrain.mutateWeights(0.8)
                # birds = birds + [Bird.Bird() for i in range(populationSize-len(birds))]

        #End current generation, exit loop and return to outer loop

        #Do evolutionary tasks here before moving on to next generation
        '''
        deadBirds.sort(key=lambda x: x.fitness, reverse=True) #sort birds by best fitness           

        #if all birds are bad just make a new set from scratch
        if deadBirds[0].fitness < 2:
            birds = [Bird.Bird() for bird in range(populationSize)]
        else:
            birds = []
            for i in range(populationSize):
                inputLayerBias, weightsInputToHidden, hiddenLayerBias, weightsHiddenToOutput = deadBirds[0].birdBrain.getGenotype()
                goodBird = Bird.Bird()
                goodBird.birdBrain.inputLayerBias = inputLayerBias[:]
                goodBird.birdBrain.weightsInputToHidden = weightsInputToHidden[:]
                goodBird.birdBrain.hiddenLayerBias = hiddenLayerBias[:]
                goodBird.birdBrain.weightsHiddenToOutput = weightsHiddenToOutput[:]
                if len(birds) == 0:
                    birds.append(goodBird)
                else:
                    if deadBirds[0].fitness < 9:
                        goodBird.birdBrain.mutateWeights(0.99)
                        birds.append(goodBird)
                    elif gameScore > 1 and gameScore < 7:
                        goodBird.birdBrain.mutateWeights(0.50)
                        birds.append(goodBird)
                    elif gameScore > 7:
                        goodBird.birdBrain.mutateWeights(0.10)
                        birds.append(goodBird)     
        '''           
        
        currentGeneration = currentGeneration + 1
        if gameScore > highScore:
            highScore = gameScore
        birds = ga.GenerateNewPopulation(populationSize).nextGeneration
    #TODO: assess fitness, pick best candidates, crossover+mutate, generate new generation



if __name__ == "__main__":

    birdEvolution()