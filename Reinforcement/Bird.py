import pygame
from math import pow
from math import tan
from math import cos
from math import sin
from math import pow
from math import sqrt
from math import pi

class Bird:
    # Sprites = [BirdWingUpSprite,BirdCruisingSprite,BirdWingDownSprite]
    BirdWingUpSprite = pygame.image.load('../images/bird1.png')
    BirdCruisingSprite = pygame.image.load('../images/bird2.png')
    BirdWingDownSprite = pygame.image.load('../images/bird3.png')
    RotationMax = 25
    RotationVelocity = 20
    AnimationTime = 5

    def __init__(self):
        self.positionX = 150
        self.positionY = 250
        # self.angleOfPitch = 0
        # self.time = 0
        self.velocityY = 0
        self.currentSpriteCount = 0
        self.currentSprite = self.BirdCruisingSprite
        self.died = False
        # self.reward = None

    def jump(self):

        self.velocityY = self.velocityY - 2
        if self.velocityY < -16:
            self.velocityY = -16
        elif self.velocityY > 16:
            self.velocityY = 16

        
    def jumpKey(self):
        self.velocityY = self.velocityY - 4


    def update(self):
        #horizontal velocity = 5
        # self.time = self.time + 1
        # gravity = 2.5
        # deltaY = 0.5 * gravity #ignore the time variable because calculating per unit time
        # self.posY = self.posY + deltaY
        gravity = 0.1
        self.velocityY = self.velocityY + gravity
        self.positionY = self.positionY + self.velocityY
        if self.positionY < 0:
            self.positionY = 0
        


    def draw(self,window):
        
        window.blit(self.currentSprite,(self.positionX,self.positionY))


    def getMask(self):

        return pygame.mask.from_surface(self.currentSprite)