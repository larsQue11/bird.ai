import pygame
import time
import random
import NeuralNetwork as nn
import NewBird as Bird
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


def drawWindow(window,bird,pipes,base,score):
    window.blit(BackgroundImage,(0,0))

    for pipe in pipes:
        pipe.draw(window)

    text = Font.render(f"Score: {score}",True,(255,255,255))
    window.blit(text,(10,10))
    base.draw(window)
    
    bird.draw(window)
    # for bird in birds:
    #     bird.draw(window)
    pygame.display.update()


def generatePipe(distance):

    distance = distance + random.randint(250,400)
    return Pipe(distance)


def birdEvolution():
    
    stillLearning = True
    while stillLearning:

        #Following represents a single generation of evolution
        window = pygame.display.set_mode((WindowWidth,WindowHeight))
        base = Base()
        gameScore = 0
        pipesPassed = 0
        gameObjects = [Pipe(400 * i) for i in range(1,20)]
        nextObject = gameObjects[pipesPassed]
        generation = True
        bird = Bird.Bird()
        while generation:
            pygame.time.delay(30)
            drawWindow(window,bird,gameObjects,base,gameScore)
            for event in pygame.event.get():
                # gameClock.tick(30)
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_ESCAPE :
                        run = False
                    elif event.key == pygame.K_SPACE :
                        bird.jump()
                elif event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            for obj in gameObjects:
                obj.move()

            base.move()
            bird.update()
            if nextObject.collide(bird):
                print("Pipe collision")
                bird.fitness = bird.fitness + gameScore
                bird.died = True
                            

            # check for base collision, bird dies if true
            if bird.positionY >= 400:
                print("Base collision")
                bird.fitness = bird.fitness + gameScore
                bird.died = True
                
            if nextObject.posX < bird.positionX:
                gameScore = gameScore + 1
                pipesPassed = pipesPassed + 1
                nextObject = gameObjects[pipesPassed]
                gameObjects.append(generatePipe(gameObjects[len(gameObjects)-1].posX))
        #End current generation, exit loop and return to outer loop

    #TODO: assess fitness, pick best candidates, crossover+mutate, generate new generation



if __name__ == "__main__":

    birdEvolution()