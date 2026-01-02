import pygame,random
from pygame.locals import *
from goodFormations import *
from evilFormations import *
from soldiers import *

SIZE = (500,500)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED  = (255,0,0)
GREEN = (0,255,0)


        
                    

def init():
    '''Returns Screen and font, no args
    '''
    #required stuff
    pygame.init()
    pygame.font.init()

    
    screen = pygame.display.set_mode((SIZE[0],SIZE[1]))
    font = pygame.font.Font('freesansbold.ttf', 20)
    return screen,font

def drawGrid(screen):
    #Only for placing
    for x in range(SIZE[0]//10):
        pygame.draw.line(screen,BLACK,(x*10,0),(x*10,SIZE[1]))
    for y in range(SIZE[1]//10):
        pygame.draw.line(screen,BLACK,(0,y*10),(SIZE[1],y*10))


def main():
    screen,font = init()

    form = SquareFormation(x=10,y=10,pos=(12,10),num=100,side='Good',color=GREEN)
    enemy = Barbarian(x=20,y=20,pos=(20,50),num=350,side='Bad',color = RED)

    world = [form,enemy]
    current = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    world[current%(len(world))].tick(world)
                    current += 1



        screen.fill(WHITE)
        for i in world:
            i.render(screen)
        drawGrid(screen)
 
        
        pygame.display.update()
    

if __name__ == '__main__':main()
