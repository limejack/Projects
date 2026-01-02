import pygame,time
from pygame.locals import *

class Dinosaur():
    def __init__(self):
        self.pos = (5,GROUNDLINE-20)
        self.isJumping = False
        self.velocity = 0
        self.rect = self.pos+(10,20)

    def render(self,screen,keys):
        if K_DOWN in keys and not self.isJumping:
            self.pos = (5,GROUNDLINE-10)
            self.rect = pygame.draw.rect(screen,BLACK,self.pos+(20,10))
        else:
            self.rect = pygame.draw.rect(screen,BLACK,self.pos+(10,20))

    def tick(self,timeChange,keys):
        if self.isJumping:
            self.velocity += 8000*timeChange
            if K_DOWN in keys:
                self.velocity = 4000
            self.pos = (self.pos[0],self.pos[1]+self.velocity*timeChange)
        if self.pos[1] > GROUNDLINE-20:
            self.pos = (self.pos[0],GROUNDLINE-20)
            self.isJumping = False
            self.velocity = 0
    def jump(self):
        if not self.isJumping:
            self.isJumping = True
            self.velocity = -1000

class Cactus():
    def __init__(self,h,w,x):
        self.pos = (x,GROUNDLINE-h)
        self.dimensions = (h,w)
        self.rect = self.pos+(h,w)

    def render(self,screen):
        self.rect = pygame.draw.rect(screen,BLACK,self.pos+self.dimensions)
    def tick(self,speed,timeChange):
        self.pos = (self.pos[0]-timeChange*speed,self.pos[1])
        

SIZE = (500,500)
WHITE = (255,255,255)
BLACK = (0,0,0)
GROUNDLINE = 250
DISTANCE = 300

def init():
    screen = pygame.display.set_mode(SIZE)
    return screen

def drawGroundline(screen):
    pygame.draw.line(screen,BLACK,(0,GROUNDLINE),(SIZE[0],GROUNDLINE))

def main():
    screen = init()

    player =  Dinosaur()
    keysDown = set()

    obsticles = [Cactus(10,10,SIZE[0])]

    done = False

    remove = False
    lastTick = time.time()
    t = time.time()
    while not done:
        #with open('text.txt','a') as file:file.write(str(t)+'\n')
        lastTick = time.time()
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    player.jump()
                keysDown.add(event.key)
            if event.type == KEYUP:
                keysDown.remove(event.key)
            
        drawGroundline(screen)
        player.render(screen,keysDown)

        for obs in obsticles:
            obs.render(screen)
            obs.tick(500,time.time()-lastTick)
            if obs.pos[0] + obs.dimensions[0] < 0:
                remove = True
            if time.time()-t > 1 and player.rect.colliderect(obs.rect):
                print('GAMEOVER')
                done = True
                t = time.time()
        if remove:
            remove = obsticles[1:]
            remove = False

        if SIZE[0] - obs.pos[0] > DISTANCE:
            obsticles.append(Cactus(10,10,obs.pos[0]+DISTANCE))
                
        player.tick(time.time()-lastTick,keysDown)
        
        pygame.display.update()


    ##END OF GAME
    while True:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        drawGroundline(screen)
        player.render(screen,keysDown)

        for obs in obsticles:
            obs.render(screen)                
        
        pygame.display.update()
    


if __name__ == '__main__':main()
