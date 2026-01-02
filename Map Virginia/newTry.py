class Building():
    def __init__(self,pos,party,color):
        self.pos = pos
        self.party = party
        self.color = color

import pygame,sys,random,math
from pygame.locals import *

random.seed(0)

def generateBuildings(n=100):
    out = []
    colors = [(255,0,0),(0,0,255)]
    for i in range(n):
        pos = (random.random(),random.random())
        party = random.randint(0,1)
        out.append(Building(pos,party,colors[party]))
    return out
def drawBuildings(screen,rect,houses):
    for i in houses:
        pygame.draw.circle(screen,i.color,(rect[2]*i.pos[0]+rect[0],rect[3]*i.pos[1]+rect[1]),2)
def getClosestFromDistrict(houses,district,point):
    minDist = math.inf
    minHouse = -1
    for i in houses:
        if i in district:
            continue
        dist = getDist(i,point)
        if dist < minDist:
            minDist = dist
            minHouse = i
    return minHouse
def getDist(a,b):
    return (a.pos[0]-b.pos[0])**2+(a.pos[1]-b.pos[1])**2

screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

houses = generateBuildings()
drawBuildings(screen,(0,0,500,500),houses)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
