import pygame
import time
import random
import NeuralNetwork as nn
import Bird


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
        # self.gap = 0
        self.top = 0
        self.bottom = 0
        self.TopPipe = pygame.transform.flip(self.PipeSprite, False, True)
        self.BottomPipe = self.PipeSprite

        self.pipePassed = False
        self.setHeight()

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

        offset1 = (self.x1 - bird.posX, 112 - round(bird.posY))
        offset2 = (self.x2 - bird.posX, 112 - round(bird.posY))

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
    pygame.display.update()


def main():
    bird = Bird.Bird(230,250)
    base = Base(400)
    pipes = [Pipe(400)]
    window = pygame.display.set_mode((WindowWidth,WindowHeight))
    gameClock = pygame.time.Clock()

    gameScore = 0

    run = True
    while run:
        gameClock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        addPipe = False
        pipeBin = [] #a bin to throw away surpassed pipes
        for pipe in pipes:

            #check if the bird collides with the pipe, end game if True
            if pipe.collide(bird):
                pass

            if pipe.posX + pipe.TopPipe.get_width() < 0: #is pipe off screen?
                pipeBin.append(pipe)

            if not pipe.pipePassed and pipe.posX < bird.posX:
                pipe.pipePassed = True
                addPipe = True

            pipe.move()

        if addPipe:
            gameScore = gameScore + 1
            pipes.append(Pipe(900)) #place next pipe on screem
        
        pipeBin[:] = []

        #base collision
        if bird.posY + bird.currentSprite.get_height() >= 730:
            pass

        base.move()
        drawWindow(window,bird,pipes,base,gameScore)
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()