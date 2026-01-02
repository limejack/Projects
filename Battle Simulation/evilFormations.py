import goodFormations
import random,pygame
from soldiers import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED  = (255,0,0)

class Barbarian(goodFormations.SquareFormation):
    def __init__(self,soldiers=None,x=-1,y=-1,pos=None,num=10,side='',color=(1,1,1)):
        super().__init__((soldiers,x,y,pos,num))
        self.side = side
        self.still = True
        
        if soldiers == None:
            self.generateSoldiers(num,pos,x,y)
        else:
            self.soldiers = soldiers

        self.pos = pos
        self.color = color
    def render(self,screen):
        for s in self.soldiers:
            s.render(screen,self.color)

    def generateSoldiers(self,num,pos,x,y):
        self.soldiers = []
        used =[]
        for i in range(num):
            p = (random.randint(pos[0],pos[0]+x),random.randint(pos[1],pos[1]+y))
            while p in used:p = (random.randint(pos[0],pos[0]+x),random.randint(pos[1],pos[1]+y))
            used.append(p)
            self.soldiers.append(Soldier(*p,self,self.side))
    
    def tick(self,world):
        if len(self.soldiers) == 0:
            return
        targets = set()

        for s in self.soldiers:
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


        
        for s in self.soldiers:
            s.tick(world)
            

        for s in self.soldiers:
            s.move = s.maxMove
            s.hasMoved = False
            s.attacks = s.maxAttacks
class SmartVillain(goodFormations.SquareFormation):
    def __init__(self,soldiers=None,x=-1,y=-1,pos=None,num=10,side='',color=(1,1,1)):
        super().__init__((soldiers,x,y,pos,num))
        self.side = side
        self.still = True
        numLayers = 4
        self.shape = [[0 for i in range(num//numLayers)] for j in range(numLayers)]
        self.pos = pos
        
        if soldiers == None:
            self.generateSoldiers(num,pos,x,y)
        else:
            self.soldiers = soldiers

        self.pos = pos
        self.color = color
    def render(self,screen):
        for s in self.soldiers:
            s.render(screen,self.color)

    def generateSoldiers(self,num,pos,x,y):
        self.soldiers = []
        used =[]
        locations = []
        for i in range(len(self.shape)):
            locations.append([])
            for j in range(len(self.shape[i])):
                self.soldiers.append(Soldier(j+self.pos[0],i+self.pos[1],self,self.side))
                locations[-1].append(self.soldiers[-1])
    
    def tick(self,world):
        if len(self.soldiers) == 0:
            return
        targets = set()

        for s in self.soldiers:
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


        
        for s in self.soldiers:
            s.tick(world)
            

        for s in self.soldiers:
            s.move = s.maxMove
            s.hasMoved = False
            s.attacks = s.maxAttacks
