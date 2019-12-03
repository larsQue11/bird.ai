import pygame
from math import pow

class Bird:
    # Sprites = [BirdWingUpSprite,BirdCruisingSprite,BirdWingDownSprite]
    BirdWingUpSprite = pygame.image.load('./images/bird1.png')
    BirdCruisingSprite = pygame.image.load('./images/bird2.png')
    BirdWingDownSprite = pygame.image.load('./images/bird3.png')
    RotationMax = 25
    RotationVelocity = 20
    AnimationTime = 5

    def __init__(self,x,y):
        self.posX = x
        self.posY = y
        self.angleOfPitch = 0
        self.tickCount = 0
        self.velocity = 0
        self.height = self.posY
        self.currentSpriteCount = 0
        self.currentSprite = self.BirdCruisingSprite

    def jump(self):
        self.velocity = -10.5
        self.tickCount = 0
        self.height = self.posY

    def move(self):
        
        self.tickCount = self.tickCount + 1
        delta = (self.velocity * self.tickCount) + (1.5 * pow(self.tickCount,2))
        if delta >= 16:
            delta = 16
        elif delta < 0:
            delta = delta - 2
        
        self.posY = self.posY + delta
        if delta < 0 or self.posY < self.height + 50:
            if self.angleOfPitch < self.RotationMax:
                self.angleOfPitch = self.RotationMax
        else:
            if self.angleOfPitch > -90:
                self.angleOfPitch = self.angleOfPitch - self.RotationVelocity

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