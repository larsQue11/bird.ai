import pygame
from math import pow
from math import tan
from math import cos
from math import sin
from math import pow
from math import sqrt
from math import pi
import NeuralNetwork as nn

class Bird:
    # Sprites = [BirdWingUpSprite,BirdCruisingSprite,BirdWingDownSprite]
    BirdWingUpSprite = pygame.image.load('./images/bird1.png')
    BirdCruisingSprite = pygame.image.load('./images/bird2.png')
    BirdWingDownSprite = pygame.image.load('./images/bird3.png')
    RotationMax = 25
    RotationVelocity = 20
    AnimationTime = 5

    def __init__(self):
        self.posX = 150
        self.posY = 250
        self.angleOfPitch = 0
        self.time = 0
        self.velocityY = 0
        self.currentSpriteCount = 0
        self.currentSprite = self.BirdCruisingSprite
        self.birdBrain = nn.NeuralNetwork(3,3,1)
        self.fitness = 0
        self.died = False
        self.move()

    def jump(self,inputVector):
        
        prediction = self.birdBrain.predict(inputVector)
        # print(prediction[0][0])
        if prediction[0][0] > 0.5:
            print("JUMP!")
            return True
        else:
            print("no jump")
            print(prediction[0][0])
            return False


    # def jump(self):

    #     self.velocity = -2.5
    #     self.time = 0
    #     # self.posY


    def move(self):
        #horizontal velocity = 5
        self.time = self.time + 1
        gravity = 2.5
        deltaY = 0.5 * gravity #ignore the time variable because calculating per unit time
        self.posY = self.posY + deltaY
    '''
    def move(self,inputVector):
        #horizontal velocity = 5
        self.time = self.time + 1
        gravity = 2.5
        if self.jump(inputVector):
            velocityX = 5 #horizontal velocity of game is 5
            self.velocityY = self.velocityY - 5
            if self.velocityY < -20:
                self.velocityY = -20 
            # velocityTheta = sqrt(pow(velocityX,2) - pow(velocityY,2))
            # theta = 60
            deltaY = (self.velocityY * self.time) + (0.5 * gravity * pow(self.time,2))
            # self.posY = self.posY + deltaY

        else:
            deltaY = 0.5 * gravity #ignore the time variable because calculating per unit time

        self.posY = self.posY + deltaY
        if self.posY < 0:
            self.posY = 0

        # if delta >= 16:
        #     delta = 16
        # elif delta < 0:
        #     delta = delta - 2

        # if deltaY < 0 or self.posY < self.posY + 50:
        #     if self.angleOfPitch < self.RotationMax:
        #         self.angleOfPitch = self.RotationMax
        # else:
        #     if self.angleOfPitch > -90:
        #         self.angleOfPitch = self.angleOfPitch - self.RotationVelocity
        '''


    def draw(self,window):

        self.currentSpriteCount = self.currentSpriteCount + 1
        if self.currentSpriteCount < self.AnimationTime:
            self.currentSprite = self.BirdWingUpSprite
        elif self.currentSpriteCount < self.AnimationTime*2:
            self.currentSprite = self.BirdCruisingSprite
        elif self.currentSpriteCount < self.AnimationTime*3:
            self.currentSprite = self.BirdWingDownSprite
        elif self.currentSpriteCount < self.AnimationTime*4:
            self.currentSprite = self.BirdCruisingSprite
        elif self.currentSpriteCount < self.AnimationTime*4 + 1:
            self.currentSprite = self.BirdWingUpSprite
            self.currentSpriteCount = 0

        if self.angleOfPitch <= -80:
            self.currentSprite = self.BirdCruisingSprite
            self.currentSpriteCount = self.AnimationTime * 2

        rotatedImage = pygame.transform.rotate(self.currentSprite,self.angleOfPitch)
        rotationRectangle = rotatedImage.get_rect(center=self.currentSprite.get_rect(topleft = (self.posX,self.posY)).center)
        window.blit(rotatedImage,rotationRectangle.topleft)


    def getMask(self):

        return pygame.mask.from_surface(self.currentSprite)