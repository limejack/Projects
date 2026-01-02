import random,pygame,math


WHITE = (255,255,255)
BLACK = (0,0,0)
RED  = (255,0,0)


class Soldier():
    def __init__(self,x,y,parent,side):
        self.health = 30
        self.side = side
        self.move = 6
        self.isDead = False
        self.maxMove = 6
        self.hasMoved = False
        self.x = x
        self.y = y
        self.target = None
        self.parent = parent
        self.attacks = 1
        self.maxAttacks =1
        self.name = 'Sold'
    def dist(self,a,b):
        return (a[0]-b[0])**2+(a[1]-b[1])**2
    def render(self,screen,color):
        pygame.draw.rect(screen,color,(self.x*10,self.y*10,10,10))
    def occupied(self,world):
        out = []
        for i in world:
            for s in i.soldiers:
                out.append((s.x,s.y))
        return out
    def tick(self,world):
        if not self.target:
            for unit in world:
                if unit.side == self.side:
                    continue
                for s in unit.soldiers:
                    if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                        s.health -= 5
                        if s.health <= 0:
                            s.dead = True
                            s.parent.soldiers.remove(s)

                        self.attacks -= 1
                        self.parent.keepFormation = False

            return



            
        frontier = [(self.x,self.y,0)]
        explored = set()

        o = self.occupied(world)

        closest = (None,None)
        while frontier:
            current = frontier.pop(0)
            
            if current[:-1] in explored: continue
            explored.add(current[:-1])
            
            d = self.dist(current[:-1],(self.target[0],self.target[1]))
            if not closest[1]:
                closest = (d,current[:-1],current[2])
            elif d < closest[0]:
                closest = (d,current[:-1],current[2])
                
            if current[2] == self.move:
                continue

            possibleMoves = [(current[0]+1,current[1],current[2]+1),
                         (current[0]-1,current[1],current[2]+1),
                         (current[0],current[1]+1,current[2]+1),
                         (current[0],current[1]-1,current[2]+1),
                         ]
            for i in possibleMoves:
                if i[:-1] not in o:
                    frontier.append(i)


        self.x = closest[1][0]
        self.y = closest[1][1]
        self.move -= closest[2]

        for unit in world:
            if unit.side == self.side:
                continue
            for s in unit.soldiers:
                if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                    s.health -= 5
                    if s.health <= 0:
                        s.dead = True
                        s.parent.soldiers.remove(s)

                    self.attacks -= 1
                    self.parent.keepFormation = False


        return


class Barb(Soldier):
    def __init__(self,x,y,parent,side):
        super().__init__(x,y,parent,side)
        self.name = 'barb'
        self.health = 30
        self.side = side
        self.move = 6
        self.maxMove = 6
        self.hasMoved = False
        self.x = x
        self.y = y
        self.target = None
        self.parent = parent
        self.attacks = 1
        self.maxAttacks = 1
        self.isDead = False
    def tick(self,world):
        if not self.target: return
        frontier = [(self.x,self.y,0)]
        explored = set()

        o = self.occupied(world)

        closest = (None,None)

        while frontier:
            current = frontier.pop(0)
            
            if current[:-1] in explored: continue
            explored.add(current[:-1])
            
            d = self.dist(current[:-1],(self.target[0],self.target[1]))
            if not closest[1]:
                closest = (d,current[:-1],current[2])
            elif d < closest[0]:
                closest = (d,current[:-1],current[2])
                
            if current[2] == self.move:
                continue

            possibleMoves = [(current[0]+1,current[1],current[2]+1),
                         (current[0]-1,current[1],current[2]+1),
                         (current[0],current[1]+1,current[2]+1),
                         (current[0],current[1]-1,current[2]+1),
                         ]
            for i in possibleMoves:
                if i[:-1] not in o:
                    frontier.append(i)


        self.x = closest[1][0]
        self.y = closest[1][1]
        self.move -= closest[2]

        if self.target in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
            t = None
            for unit in world:
                for s in unit.soldiers:
                    if (s.x,s.y) == self.target:
                        t = s
            if t == None: return

            t.health -= 5
            if t.health <= 0:
                t.dead = True
                t.parent.soldiers.remove(t)
            self.attacks -= 1



class Archer():
    def __init__(self,x,y,parent,side):
        self.health = 15
        self.side = side
        self.move = 6
        self.isDead = False
        self.maxMove = 6
        self.hasMoved = False
        self.x = x
        self.y = y
        self.target = None
        self.parent = parent
        self.attacks = 1
        self.maxAttacks =1
        self.name = 'Archer'
    def dist(self,a,b):
        return (a[0]-b[0])**2+(a[1]-b[1])**2
    def render(self,screen,color):
        pygame.draw.circle(screen,color,(self.x*10+5.75,self.y*10+5.75),5)
        pygame.draw.circle(screen,BLACK,(self.x*10+5.75,self.y*10+5.75),5,1)

    def occupied(self,world):
        out = []
        for i in world:
            for s in i.soldiers:
                out.append((s.x,s.y))
        return out
    def tick(self,world):
        for unit in world:
            if unit.side == self.side:
                continue
            for s in unit.soldiers:
                if math.sqrt(self.dist((s.x,s.y),(self.x,self.y)))<20000  and self.attacks > 0:
                    s.health -= 2
                    if s.health <= 0:
                        s.dead = True
                        s.parent.soldiers.remove(s)

                    self.attacks -= 1
                    self.parent.keepFormation = False


        return

class Cavalry():
    def __init__(self,x,y,parent,side):
        self.health = 60
        self.side = side
        self.move = 12
        self.isDead = False
        self.maxMove = 12
        self.hasMoved = False
        self.x = x
        self.y = y
        self.target = None
        self.parent = parent
        self.attacks = 1
        self.maxAttacks =1
        self.name = 'Calv'
        self.mounted = True
        self.isCharging = False
    def dist(self,a,b):
        return (a[0]-b[0])**2+(a[1]-b[1])**2
    def render(self,screen,color):
        if self.mounted:
            pygame.draw.circle(screen,color,(self.x*10+5.75,self.y*10+5.75),5)
            pygame.draw.circle(screen,BLACK,(self.x*10+5.75,self.y*10+5.75),5,1)
        else:
            pygame.draw.circle(screen,(0,0,255),(self.x*10+5.75,self.y*10+5.75),5)
            pygame.draw.circle(screen,BLACK,(self.x*10+5.75,self.y*10+5.75),5,1)

    def occupied(self,world):
        out = []
        for i in world:
            for s in i.soldiers:
                out.append((s.x,s.y))
        return out
    def tick(self,world):
        
        if self.health < 30:
            self.mounted = False
            self.maxMove = 3
            if self.move > 3:self.move = 3


        
        if not self.target:
            for unit in world:
                if unit.side == self.side:
                    continue
                for s in unit.soldiers:
                    if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                        s.health -= 5
                        if s.health <= 0:
                            s.dead = True
                            s.parent.soldiers.remove(s)

                        self.attacks -= 1
                        self.parent.keepFormation = False

            return



            
        frontier = [(self.x,self.y,0)]
        explored = set()

        o = self.occupied(world)

        closest = (None,None)
        while frontier:
            current = frontier.pop(0)
            
            if current[:-1] in explored: continue
            explored.add(current[:-1])
            
            d = self.dist(current[:-1],(self.target[0],self.target[1]))
            if not closest[1]:
                closest = (d,current[:-1],current[2])
            elif d < closest[0]:
                closest = (d,current[:-1],current[2])
                
            if current[2] == self.move:
                continue

            possibleMoves = [(current[0]+1,current[1],current[2]+1),
                         (current[0]-1,current[1],current[2]+1),
                         (current[0],current[1]+1,current[2]+1),
                         (current[0],current[1]-1,current[2]+1),
                         ]
            for i in possibleMoves:
                if i[:-1] not in o:
                    frontier.append(i)


        self.x = closest[1][0]
        self.y = closest[1][1]
        self.move -= closest[2]

        for unit in world:
            if unit.side == self.side:
                continue
            for s in unit.soldiers:
                if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                    if s.name == 'Pike' and self.isCharging:
                        self.health -= 30
                        self.isCharging = False
                    if self.move <= self.maxMove-10 and self.mounted or self.isCharging:
                        s.health -= 30
                    elif self.mounted:
                        s.health -= 3
                    else:
                        s.health -= 3
                    if s.health <= 0:
                        s.dead = True
                        s.parent.soldiers.remove(s)

                    self.attacks -= 1
                    self.parent.keepFormation = False
        if self.move == 0:
            self.isCharging = True
        else:
            self.isCharging = False

        return

class Pikeman():
    def __init__(self,x,y,parent,side):
        self.health = 20
        self.side = side
        self.move = 6
        self.isDead = False
        self.maxMove = 6
        self.hasMoved = False
        self.x = x
        self.y = y
        self.target = None
        self.parent = parent
        self.attacks = 1
        self.maxAttacks =1
        self.name = 'Pike'
    def dist(self,a,b):
        return (a[0]-b[0])**2+(a[1]-b[1])**2
    def render(self,screen,color):
        pygame.draw.rect(screen,(color[0],color[1],color[2]+255),(self.x*10,self.y*10,10,10))
    def occupied(self,world):
        out = []
        for i in world:
            for s in i.soldiers:
                out.append((s.x,s.y))
        return out
    def tick(self,world):
        if not self.target:
            for unit in world:
                if unit.side == self.side:
                    continue
                for s in unit.soldiers:
                    if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                        s.health -= 5
                        if s.health <= 0:
                            s.dead = True
                            s.parent.soldiers.remove(s)

                        self.attacks -= 1
                        self.parent.keepFormation = False

            return



            
        frontier = [(self.x,self.y,0)]
        explored = set()

        o = self.occupied(world)

        closest = (None,None)
        while frontier:
            current = frontier.pop(0)
            
            if current[:-1] in explored: continue
            explored.add(current[:-1])
            
            d = self.dist(current[:-1],(self.target[0],self.target[1]))
            if not closest[1]:
                closest = (d,current[:-1],current[2])
            elif d < closest[0]:
                closest = (d,current[:-1],current[2])
                
            if current[2] == self.move:
                continue

            possibleMoves = [(current[0]+1,current[1],current[2]+1),
                         (current[0]-1,current[1],current[2]+1),
                         (current[0],current[1]+1,current[2]+1),
                         (current[0],current[1]-1,current[2]+1),
                         ]
            for i in possibleMoves:
                if i[:-1] not in o:
                    frontier.append(i)


        self.x = closest[1][0]
        self.y = closest[1][1]
        self.move -= closest[2]

        for unit in world:
            if unit.side == self.side:
                continue
            for s in unit.soldiers:
                if (s.x,s.y) in [(self.x+1,self.y),(self.x-1,self.y),(self.x,self.y+1),(self.x,self.y-1)] and self.attacks > 0:
                    if s.name == 'Calv' and s.mounted:
                        s.health -= 5
                    else:
                        s.health -= 2
                    if s.health <= 0:
                        s.dead = True
                        s.parent.soldiers.remove(s)

                    self.attacks -= 1
                    self.parent.keepFormation = False


        return

