import random,pygame
from soldiers import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED  = (255,0,0)


class SquareFormation():
    def __init__(self,soldiers=None,x=-1,y=-1,pos=None,num=10,side='',color=(255,0,0)):
        self.still = True
        self.side = side
        self.keepFormation = True
        
        num -= 20
        numRows = 3
        self.shape = [[0 for i in range(num//numRows)] for j in range(numRows)]
        self.pos = pos
        self.holdback = []
        self.archers = []
    
        if soldiers == None:
            self.generateSoldiers(num,pos,x,y)
        else:
            self.soldiers = soldiers
        self.color = color
        self.countoff = 0

        
    def generateSoldiers(self,num,pos,x,y):
        self.soldiers = []
        used =[]
        locations = []
        #for i in range(len(self.shape)):
        #    locations.append([])
        #    for j in range(len(self.shape[i])):
        #        self.soldiers.append(Soldier(j+self.pos[0],i+self.pos[1],self,self.side))
        #        locations[-1].append(self.soldiers[-1])
        for i in range(len(locations)):
            for j in range(0):
                self.soldiers.remove(locations[i][j])
                self.soldiers.append(Archer(j+self.pos[0],i+self.pos[1],self,self.side))
                locations[i][j] = self.soldiers[-1]
                self.holdback.append(locations[i][j])
                locations[i][j].x -= 10
                locations[i][j].y += 5
                self.soldiers.remove(locations[i][-(j+1)])
                self.soldiers.append(Archer(locations[i][-(j+1)].x,locations[i][-(j+1)].y,self,self.side))
                locations[i][-(j+1)] = self.soldiers[-1]
                locations[i][-(j+1)].x += 10
                locations[i][-(j+1)].y += 5
                self.holdback.append(self.soldiers[-1])

        for i in range(40):
            for j in range(5):
                self.archers.append(Archer(i+self.pos[0]-10,j+self.pos[1]-10,self,self.side))
                self.soldiers.append(self.archers[-1])

        print(len(self.soldiers))
        
    def render(self,screen):
        for s in self.soldiers:s.render(screen,self.color)
    def dist(self,a,b):
        return (a[0]-b[0])**2+(a[1]-b[1])**2
    def findNearestSoldier(self,pos,rank,group):
        lowerRanks = []
        for s in self.groups[group]:
            if (not s.target or self.shape[s.target[1]][s.target[0]] < rank) and not s.hasMoved:
                lowerRanks.append(s)

        if not lowerRanks:return None
        closest = self.dist((lowerRanks[0].x,lowerRanks[0].y),(pos[0]+self.pos[0],pos[1]+self.pos[1]))
        out = lowerRanks[0]
        
        for s in lowerRanks:
            d = self.dist((s.x,s.y),(pos[0]+self.pos[0],pos[1]+self.pos[1]))
            if d < closest:
                closest = d
                out = s
        return out
    def scatter(self,world):
        for s in self.soldiers:
            if self.countoff < 4 and s in self.holdback:
                continue
            if s in self.archers:
                continue
            minDist = ()
            for unit in world:
                if unit.side == self.side:
                    pass
                else:
                    for e in unit.soldiers:
                        if not minDist or self.dist((e.x,e.y),(s.x,s.y)) < minDist[0]:
                            minDist = (self.dist((e.x,e.y),(s.x,s.y)),(e.x,e.y))
            if not minDist:
                continue
            s.target= minDist[1]


    def tick(self,world):
        if not self.keepFormation:
            self.scatter(world)
            self.countoff += 1

        for s in self.soldiers:
            s.tick(world)



        for s in self.soldiers:
            s.move = s.maxMove
            s.hasMoved = False
            s.attacks = s.maxAttacks

