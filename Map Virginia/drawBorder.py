def getBorders():
    return eval(open('borders.txt').read())
def drawBorder(county,screen):
##    for lat,long in county:
##        pygame.draw.circle(screen,(0,0,0),(lat,long),1)
##        pygame.display.update()
    pygame.draw.polygon(screen,randomColor(),county)        
def randomColor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

import pygame,sys,random
from pygame.locals import *

screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

borders = getBorders()
sides = [36.54213065200002, -83.59094398599996, 39.42581624300004, -75.34102361099998]
counties = list(borders.keys())

index = 1

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if index < len(counties):
        drawBorder(borders[counties[index]],screen)    
        index += 1

    pygame.display.update()
