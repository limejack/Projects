class Boat():
    def __init__(self,size,start,direction):
        self.tiles = []
        self.direction = direction
        self.size = size
        if direction == 0:
            for x in range(start[0],size+start[0]):
                self.tiles.append((x,start[1]))
        else:
            for y in range(start[1],size+start[1]):
                self.tiles.append((start[0],y))


import pygame,sys,random
from pygame.locals import *

#Global Vars
TOPMARGIN = 50
SIZE      = (500,500)
BLACK     = (0,0,0)
BLUE      = (0,0,255)
GREEN     = (0,255,0)
WHITE     = (255,255,255)
RED       = (255,0,0)

#Initiate vars
def init():
    '''Returns Screen and font, no args
    '''
    #required stuff
    pygame.init()
    pygame.font.init()

    
    screen = pygame.display.set_mode((SIZE[0],SIZE[1]+TOPMARGIN))
    font = pygame.font.Font('freesansbold.ttf', 20)
    return screen,font

def drawGrid(screen):
    for x in range(1,10):
        pygame.draw.line(screen,BLACK,(x*SIZE[0]/10,TOPMARGIN),(x*SIZE[0]/10,SIZE[1]+TOPMARGIN))
    for y in range(10):
        pygame.draw.line(screen,BLACK,(0,TOPMARGIN+y*SIZE[1]/10),(SIZE[1],TOPMARGIN+y*SIZE[1]/10))

def drawHits(screen,hit,miss,t):
    for pos in hit[t-1]:
        pygame.draw.circle(screen,RED,(pos[0]*SIZE[0]//10+SIZE[0]//20,pos[1]*SIZE[1]//10 +SIZE[1]//20+ TOPMARGIN),SIZE[0]//20)
    for pos in miss[t-1]:
        pygame.draw.circle(screen,WHITE,(pos[0]*SIZE[0]//10+SIZE[0]//20,pos[1]*SIZE[1]//10 +SIZE[1]//20+ TOPMARGIN),SIZE[0]//20)
    
#Called every iteration
def turn(t,screen,font,hits,hasHits,hasMissed):
    done = False
    text = font.render('Miss, press enter to continue',True,WHITE)
    textRect = text.get_rect()
    while True:
        screen.fill(BLUE)
        if done:
            screen.blit(text,textRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not done:
                pos = (event.pos[0]//(SIZE[0]//10),(event.pos[1]-TOPMARGIN)//(SIZE[1]//10))
                if pos not in hasHits[t-1]:
                    if pos in hits[t-1]:
                        hasHits[t-1].add(pos)
                        hits[t-1].remove(pos)
                        if not len(hits[t-1]):
                            return
                        #done = True
                    else:
                        hasMissed[t-1].add(pos)
                        done = True
            if event.type == KEYDOWN:
                if event.key == K_RETURN and done:
                    return
                        
                
        drawHits(screen,hasHits,hasMissed,t)
        drawGrid(screen)
        pygame.display.update()
def drawShips(ships,screen):
    for s in ships:
        if s.direction == 1:
            pygame.draw.rect(screen,GREEN,(s.tiles[0][0]*SIZE[0]/10+SIZE[0]/40,             #Same as below
                                           s.tiles[0][1]*SIZE[1]/10+TOPMARGIN+SIZE[1]/40,   #Positoin + TOPMARGIN + a quarter of a block
                                           SIZE[0]//20,                                     #Half the width of a tile
                                           SIZE[1]*s.size/10-SIZE[1]/20))                   #Width of s.size tiles, - half a tile
        elif s.direction == 0:
            pygame.draw.rect(screen,GREEN,(s.tiles[0][0]*SIZE[0]/10+SIZE[0]/40,             #Same as below
                                           s.tiles[0][1]*SIZE[1]/10+TOPMARGIN+SIZE[1]/40,   #Positoin + TOPMARGIN + a quarter of a block
                                           SIZE[1]*s.size/10-SIZE[1]/20,
                                           SIZE[0]//20))                   #Width of s.size tiles, - half a tile
    
def generateShips():
    ships = [          Boat(5,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(4,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(3,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(3,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(2,(random.randint(0,9),random.randint(0,9)),1)]
    while not checkOverlap(ships):
            ships = [Boat(5,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(4,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(3,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(3,(random.randint(0,9),random.randint(0,9)),1),
                       Boat(2,(random.randint(0,9),random.randint(0,9)),1)]
    return ships

def checkOverlap(ships):
    for i in ships:
        for j in ships:
            if i != j:
                for a in i.tiles:
                    if a in j.tiles:
                        return False
    for i in ships:
        for tile in i.tiles:
            if tile[0] >= 10 or tile[1] >= 10 or tile[0] < 0 or tile[1] < 0:
                return False
    return True

def placeShips(screen,font,t):
    ships = generateShips()
    click = False
    movingShip = (-1,None)
    text = font.render(f'Player {t}, place your ships',True,WHITE)
    textRect = text.get_rect()
    textRect.topleft = (0,0)
    enterText = font.render('Press Enter to Finish',True,WHITE)
    enterRect = enterText.get_rect()
    enterRect.topleft = (0,TOPMARGIN-enterRect.height)
    while True:
        screen.fill(BLUE)
        screen.blit(text,textRect)
        screen.blit(enterText,enterRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                click = True
                pos = (event.pos[0]//(SIZE[0]//10),(event.pos[1]-TOPMARGIN)//(SIZE[1]//10))
                for s in enumerate(ships):
                    if pos in s[1].tiles:
                        movingShip = s
                if movingShip == (-1,None):
                    click = False
            if event.type == MOUSEBUTTONUP:
                if click:
                    temp = ships[movingShip[0]]
                    ships[movingShip[0]] = Boat(movingShip[1].size,movingShip[1].tiles[0],~movingShip[1].direction + 2)
                    if not checkOverlap(ships):
                        ships[movingShip[0]] = temp
                    
                movingShip = (-1,None)
                click = False
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return ships
                    
            if event.type == MOUSEMOTION and event.buttons != (0,0,0):
                click = False
                if movingShip != (-1,None):
                    temp = (event.pos[0]//(SIZE[0]//10),(event.pos[1]-TOPMARGIN)//(SIZE[1]//10))
                    t = ships[movingShip[0]]
                    ships[movingShip[0]] = Boat(movingShip[1].size,temp,movingShip[1].direction)
                    if not checkOverlap(ships):
                        ships[movingShip[0]] = t
                    
                    
        drawShips(ships,screen)
        drawGrid(screen)


        pygame.display.update()

def waitScreen(screen,t,font):
    text = font.render(f'Player {t}, press any button to continue',True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SIZE[0]//2,SIZE[1]//2)
    while True:
        screen.fill(BLUE)
        screen.blit(text,textRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return
        pygame.display.update()
def winScreen(screen,t,font):
    text = font.render(f'Player {t}, WINSSSSSS',True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SIZE[0]//2,SIZE[1]//2)
    while True:
        screen.fill(BLUE)
        screen.blit(text,textRect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def main():
    screen,font = init()

    t = 1

    ships1 = placeShips(screen,font,t)
    t += 1
    waitScreen(screen,t,font)
    ships2 = placeShips(screen,font,t)
    t = 1
    waitScreen(screen,t,font)

    hits1 = set()
    hits2 = set()

    for i in ships1:
        for a in i.tiles:
            hits1.add(a)
    for i in ships2:
        for a in i.tiles:
            hits2.add(a)
    hasHits = [set(),set()]
    hasMissed = [set(),set()]

    while True:
        turn(t,screen,font,[hits2,hits1],hasHits,hasMissed)
        if not [hits2,hits1][t-1]:
            winScreen(screen,t,font)

        t = ~t+4

        waitScreen(screen,t,font)
        
if __name__ == '__main__':main()
