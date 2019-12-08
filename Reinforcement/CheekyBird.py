import pygame
import time
import random
import Bird as Bird
import numpy as np
import QLearning as Q

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
BackgroundImage = pygame.image.load('../images/background.png')
pygame.font.init()
Font = pygame.font.Font("../LuckiestGuy.ttf", 26)


class Pipe:
    PipeSprite = pygame.image.load('../images/pipe.png')
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
    GroundSprite = pygame.image.load('../images/ground.png')
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


def drawWindow(window,bird,pipes,base,text):
    window.blit(BackgroundImage,(0,0))

    for pipe in pipes:
        pipe.draw(window)

    text = Font.render(f"Generation: {text[0]} High Score: {text[1]} Current Score: {text[2]}",True,(255,255,255))
    # text = [Font.render(f"Generation: {text[0]}",True,(255,255,255)), Font.render(f"High Score: {text[1]}",True,(255,255,255)), Font.render(f"Current Score: {text[2]}",True,(255,255,255))]
    window.blit(text,(10,10))
    base.draw(window)
    
    bird.draw(window)
    # for bird in birds:
    #     bird.draw(window)
    pygame.display.update()


def generatePipe(distance):

    distance = distance + random.randint(250,400)
    return Pipe(distance)


def birdLearning():
    
    gameClock = pygame.time.Clock()
    stillLearning = True
    currentIteration = 0
    highScore = 0
    brain = Q.Learning()

    while stillLearning:

        #Following represents a single generation of evolution
        window = pygame.display.set_mode((WindowWidth,WindowHeight))
        base = Base()
        gameScore = 0
        pipesPassed = 0
        gameObjects = [Pipe((400 * i)) for i in range(1,20)]
        nextObject = gameObjects[pipesPassed]
        iterate = True
        
        epsilon = 1
        bird = Bird.Bird()
        
        updateTable = False
        reward = 0
        while iterate:
            
            #time control
            # gameClock.tick(30)
            # pygame.time.delay(30)
            
            for event in pygame.event.get():
                # gameClock.tick(30)
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        run = False
                    elif event.key == pygame.K_SPACE :
                        bird.jump()
                        # for bird in birds:
                        #     bird.jumpKey()
                elif event.type == pygame.QUIT:
                    brain.saveState()
                    run = False
                    pygame.quit()
                    quit()
            
            #game stuff
            drawWindow(window,bird,gameObjects,base,[currentIteration,highScore,gameScore])
            for obj in gameObjects:
                obj.move()

            base.move()

            if nextObject.collide(bird):
                print("Pipe collision")
                bird.died = True
                iterate = False
                if bird.positionY == 0:
                    reward = -1000
                else:
                    reward = -10


            # check for base collision, bird dies if true
            elif bird.positionY >= 400:
                print("Base collision")
                bird.died = True
                iterate = False
                reward = -10


            #get the current state and find the suggested action to take
            deltaX = int (nextObject.posX - bird.positionX)
            deltaY = int (nextObject.centerOfGap - bird.positionY) + 250
            
            if updateTable:
                brain.updateFromExploration(deltaX,deltaY,reward)
                updateTable = False
            
            if random.random() < epsilon:
                action = brain.explore(deltaX,deltaY)
                updateTable = True
            else:
                action = brain.exploit(deltaX,deltaY)
            
            if action == 1:
                bird.jump()

            bird.update()

                
            if nextObject.posX < bird.positionX:
                gameScore = gameScore + 1
                pipesPassed = pipesPassed + 1
                nextObject = gameObjects[pipesPassed]
                gameObjects.append(generatePipe(gameObjects[len(gameObjects)-1].posX))
                reward = 10
            

        #End current iteration, exit loop and return to outer loop
     
        currentIteration = currentIteration + 1
        if gameScore > highScore:
            highScore = gameScore
    #TODO: assess fitness, pick best candidates, crossover+mutate, generate new generation



if __name__ == "__main__":

    birdLearning()