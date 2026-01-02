import pygame,sys,time,random
from math import sin,cos,pi,sqrt
from pygame.locals import *
#Traffic Simulation
pygame.font.init()
font1 = pygame.font.SysFont('freesanbold.ttf', 15)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
SCREEN_SIZE = (400,400)

class Map():
    def __init__(self):
        self.graph = []
        self.lanes = {}
        self.points = {}
    def addLane(self,lane):
        intersectionLanes = []
        self.points[lane] = {}            

        pointsOnLine = []

        for l in self.lanes:
            point = l.intersection(lane)
            if type(point) != str:
                intersectionLanes.append(l)
            else:
                continue
            self.graph.append(IntersectionNode(point,{},[lane,l]))
            pointsOnLine.append(self.graph[-1])
            for otherLane in self.lanes[l]:
                if (otherLane.coord - lane.coord)* l.direction > 0:
                    self.graph[-1].addChild(self.points[l][otherLane])
                else:
                    self.points[l][otherLane].addChild(self.graph[-1])


            self.lanes[l].append(lane)
            self.points[l][lane] = self.graph[-1]
            self.points[lane][l] = self.graph[-1]

        temp = sorted(pointsOnLine,key=lambda x:x.getCoord(lane.orientation),reverse=lane.direction<0)
        for i in range(len(temp)-1):
            temp[i].addChild(temp[i+1])
            
        self.lanes[lane] = intersectionLanes
    def addPoint(self,point,lane):
        self.graph.append(IntersectionNode(point,{},[lane]))
        for otherLane in self.lanes[lane]:
            p = self.points[lane][otherLane]
            if (otherLane.coord - self.graph[-1].getCoord(lane.orientation))* lane.direction > 0:
                self.graph[-1].addChild(p)
            else:
                p.addChild(self.graph[-1])
    def pointAt(self,pos):
        for i in self.graph:
            if i.parent == pos:
                return i
        return False
        
    def bfs(self,goal):
        frontier = [(self.graph[0],[self.graph[0]])]
        explored = []
        goal = goal.parent
        while frontier:
            current = frontier.pop(0)
            if current[0].parent == goal:
                return current[1]
            explored.append(current[0])
            for child in current[0].children:
                if child not in explored:
                    frontier.append((child,current[1]+[child]))
        return False
        
class IntersectionNode():
    def __init__(self,pos,children,lanes=[]):
        self.parent = pos
        self.children = children
        self.lanes = lanes
    def getCoord(self,orientation):
        if orientation == 'horizontal':
            return self.parent[0]
        elif orientation == 'vertical':
            return self.parent[1]
    def addChild(self,child):
        dist = self.distance(self.parent,child.parent)
        self.children[child] = dist
        
    def distance(self,p1,p2):
        return sqrt((p1[0]-p2[0])**2 +(p1[1]-p2[1])**2)
    def render(self,screen):
        pygame.draw.rect(screen,RED,(self.parent[0]-5,self.parent[1]-5,10,10))
class Lane():
    def __init__(self,coord,width,orientation,direction,speedLimit,genRate=0):#generate is in seconds per car
        self.coord = coord
        self.width = width
        self.orientation = orientation
        self.cars = []
        self.direction = direction
        self.speedLimit = speedLimit
        self.genRate = genRate
        self.genTicker = 0
    def __str__(self):
        return str(self.coord) + " " + self.orientation
    def renderLines(self,screen):
        if self.orientation == 'vertical':
            pygame.draw.line(screen,BLACK,(self.coord-self.width/2,0),(self.coord-self.width/2,SCREEN_SIZE[1]))
            pygame.draw.line(screen,BLACK,(self.coord+self.width/2,0),(self.coord+self.width/2,SCREEN_SIZE[1]))
        elif self.orientation == 'horizontal':
            pygame.draw.line(screen,BLACK,(0,self.coord-self.width/2),(SCREEN_SIZE[1],self.coord-self.width/2))
            pygame.draw.line(screen,BLACK,(0,self.coord+self.width/2),(SCREEN_SIZE[1],self.coord+self.width/2))
    def renderCars(self,screen):
        for car in self.cars:
            car.render(screen)

    def update(self,deltaT,startTime):
        for car in self.cars:
            car.update(deltaT)
        if time.time() - startTime > self.genTicker:
            if random.randint(0,100) <= self.genRate:
                XYcoord = 1
                if self.orientation == 'horizontal':
                    XYcoord = 0
                if not self.cars:
                    self.addCar(0 if self.direction > 0 else SCREEN_SIZE[XYcoord],self.speedLimit)
                elif self.direction > 0:
                    self.addCar(min(self.cars[-1].pos[XYcoord]-100,0),self.speedLimit)
                elif self.direction < 0:
                    self.addCar(max(self.cars[-1].pos[XYcoord]+100,SCREEN_SIZE[XYcoord]),self.speedLimit)
            self.genTicker += 1
            
    def addCar(self,pos,velocity,otherCar=None):
        if self.orientation == 'vertical':
            index = len(self.cars)
            for i in range(len(self.cars)):
                if self.cars[i].pos[1]*self.direction < pos*self.direction:
                    index = i
                    break
            if otherCar:
                self.cars.insert(index,otherCar)
                otherCar.pos = (self.coord,pos)
                otherCar.velocity = Vector(90,velocity*self.direction)
            else:
                self.cars.insert(index,Car((self.coord,pos),Vector(90,velocity*self.direction)))
        elif self.orientation == 'horizontal':
            index = len(self.cars)
            for i in range(len(self.cars)):
                if self.cars[i].pos[0]*self.direction < pos*self.direction:
                    index = i
                    break
            if otherCar:
                self.cars.insert(index,otherCar)
                otherCar.pos = (pos,self.coord)
                otherCar.velocity = Vector(0,velocity*self.direction)

            else:
                self.cars.insert(index,Car((pos,self.coord),Vector(0,velocity*self.direction)))
        self.cars[index].lane = self
    def cleanOut(self):
        toRemove = 0
        for car in self.cars:
            if self.orientation == 'vertical':
                if (car.pos[1] > SCREEN_SIZE[1] and self.direction > 0) or (car.pos[1] < 0 and self.direction < 0):
                    toRemove += 1
            elif self.orientation == 'horizontal':
                if (car.pos[0] > SCREEN_SIZE[0] and self.direction > 0) or (car.pos[0] < 0 and self.direction < 0):
                    toRemove += 1
        for i in range(toRemove):
            del self.cars[0]
            
    def intersection(self,otherLane):
        if otherLane.orientation == self.orientation:
            return 'Sorry, these lanes do not intersect'
        if self.orientation == 'vertical':
            return (self.coord,otherLane.coord)
        elif self.orientation == 'horizontal':
            return (otherLane.coord,self.coord)
class Vector():
    def __init__(self,angle,mag):
        self.deg = angle
        self.magnitude = mag
        self.rad = angle/360 * 2*pi
        if angle == 90:
            self.i = 0
            self.j = mag
        elif angle == 0:
            self.i = mag
            self.j = 0
        else:
            self.i = mag*cos(self.rad)
            self.j = mag*sin(self.rad)
        if mag < 0:
            self.magnitude = abs(mag)
            self.deg += 180
            self.rad += pi
    def setMag(self,mag):
        if mag < 0:
            raise ValueError("magnitude negative")
        self.magnitude = mag
        if self.deg%180 == 90:
            self.i = 0
            self.j = mag
        elif self.deg == 0:
            self.i = mag
            self.j = 0
        else:
            self.i = mag*cos(self.rad)
            self.j = mag*sin(self.rad)
        if self.deg > 180:
            self.j *= -1
        if 270 > self.deg % 360 > 90:
            self.i *= -1

    def __eq__(self,other):
        return self.deg == other.deg and self.magnitude == other.magnitude
    def __str__(self):
        return str(self.magnitude)+" "+str(self.deg)

class Car():
    def __init__(self,pos,velocity=None):
        self.pos = pos
        if not velocity:
            self.velocity = Vector(0,0)
        else:
            self.velocity = velocity
        self.rect = None
        self.dead = False
        self.lane = None#defined when created
        self.length = 20
        self.width  = 10
        self.color = GREEN
        self.directions = []


    def render(self,screen):
        tempSurface = pygame.Surface((40,40))
        tempSurface.set_colorkey(WHITE)
        tempSurface.fill(WHITE)
        pygame.draw.rect(tempSurface,self.color,(10,15,20,10))
        tempSurface = pygame.transform.rotate(tempSurface,-self.velocity.deg)
        center = tempSurface.get_rect().center
        screen.blit(tempSurface,(self.pos[0]-center[0],self.pos[1]-center[1]))
        self.rect = tempSurface.get_rect()
        self.rect.center = self.pos

        text = font1.render(str(int(self.velocity.magnitude)),True,BLACK)
        textRect = text.get_rect()
        textRect.center = (self.pos[0],self.pos[1]-10)
        screen.blit(text,textRect)

    def getCollisionPoint(self,otherCar):
        if self.velocity.deg%180 == otherCar.velocity.deg%180:
            return None
        elif self.velocity.i == 0:
            m = otherCar.velocity.j/otherCar.velocity.i
            k = otherCar.pos[1]-m*otherCar.pos[0]
            return (self.pos[0],m*self.pos[0]+k)
        elif otherCar.velocity.i == 0:
            m = self.velocity.j/self.velocity.i
            k = self.pos[1]-m*self.pos[0]
            return (otherCar.pos[0],m*otherCar.pos[0]+k)
        else:
            m1 = self.velocity.j/self.velocity.i
            m2 = otherCar.velocity.j/otherCar.velocity.i
            k1 = self.pos[1]-m1*self.pos[0]
            k2 = otherCar.pos[1]-m2*otherCar.pos[0]
            x = (k1-k2)/(m2-m1)
            y = m1*x+k1
            return (x,y)
    def travelDownLine(self,point,x,y,length):
        if x != 0:
            m = y/x
        else:
            return (point[0],point[1]+length),(point[0],point[1]-length)
        px1 = -length/(sqrt(1+m*m))+point[0]
        px2 = length/(sqrt(1+m*m))+point[0]
        py1 = m*(px1-point[0])+point[1]
        py2 = m*(px2-point[0])+point[1]
        return (px1,py1),(px2,py2)

    def getTimeAndPoints(self,car,collisionPoint):
        enterPoint, exitPoint = self.travelDownLine(collisionPoint,car.velocity.i,car.velocity.j,car.lane.width/2+self.length/2)
        timeToEnter = self.distance(car.pos,enterPoint)/car.velocity.magnitude
        timeToExit = self.distance(car.pos,exitPoint)/car.velocity.magnitude
        if timeToEnter > timeToExit:
            tempa = timeToEnter
            tempb = enterPoint
            enterPoint = exitPoint
            exitPoint = tempb
            timeToEnter = timeToExit
            timeToExit = tempa
        if car.velocity.i*(enterPoint[0]-car.pos[0]) < 0 or car.velocity.j*(enterPoint[1]-car.pos[1]) < 0:
            timeToEnter *= -1
        if car.velocity.i*(exitPoint[0]-car.pos[0]) < 0 or car.velocity.j*(exitPoint[1]-car.pos[1]) < 0:
            timeToExit *= -1
            tempA = timeToEnter
            timeToEnter = timeToExit
            timeToExit = tempA
        return enterPoint,exitPoint,timeToEnter,timeToExit

    def willCollide(self,otherCar):
        laneCollisionMidPoint = self.getCollisionPoint(otherCar)
        if not laneCollisionMidPoint:
            return False
        enterPointA,exitPointA,timeToEnterA,timeToExitA = self.getTimeAndPoints(self,laneCollisionMidPoint)
        enterPointB,exitPointB,timeToEnterB,timeToExitB = self.getTimeAndPoints(otherCar,laneCollisionMidPoint)
        if timeToExitA < 0 or timeToExitB < 0:
            return False
        if timeToEnterA > timeToEnterB and timeToEnterA < timeToExitB:
            self.arriveAt(enterPointA,timeToExitB+0.1)
            return True
        elif timeToExitA > timeToEnterB and timeToExitA < timeToExitB:
            otherCar.arriveAt(enterPointB,timeToExitA+0.1)
            return True
        elif timeToEnterA < timeToEnterB and timeToExitA > timeToExitB:
            otherCar.arriveAt(enterPointB,timeToExitA+0.1)
            return True
        elif timeToEnterA == timeToEnterB:
            self.arriveAt(enterPointA,timeToExitB)
            return True
        return False
        
    def arriveAt(self,point,time):
        dist = self.distance(self.pos,point)
        self.changeVelocity(dist/time)
    def distance(self,p1,p2):
        return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def update(self,deltaT):
        if self.directions:
            point = self.directions[0]
            if len(point.lanes) < 2:
                self.directions.pop(0)
                return
            laneToTurnInto = point.lanes[1] if point.lanes[1] in self.directions[1].lanes else point.lanes[0]
            if self.distance(self.pos,point.parent) < laneToTurnInto.width:
                self.changeLane(laneToTurnInto)
                self.color = RED
                self.directions.pop(0)
            
            
        self.pos = (self.pos[0]+self.velocity.i*deltaT,self.pos[1]+self.velocity.j*deltaT)
    def changeLane(self,otherLane):
        self.lane.cars.remove(self)
        self.lane = otherLane
        indexToPlace = 0
        if self.lane.orientation == 'horizontal':
            otherLane.addCar(self.pos[0],self.lane.speedLimit,self)
        elif self.lane.orientation == 'vertical':
            otherLane.addCar(self.pos[1],self.lane.speedLimit,self)

            
    def changeVelocity(self,mag):
        if mag < 0:
            raise ValueError()
        index = self.lane.cars.index(self)
        if index == len(self.lane.cars)-1:
            self.velocity.setMag(min(self.velocity.magnitude,mag))
        else:
            self.velocity.setMag(mag)
            otherCar = self.lane.cars[index+1]
            if self.distance(self.pos,otherCar.pos) < 30:
                otherCar.changeVelocity(min(otherCar.velocity.magnitude,mag,self.velocity.magnitude))
            self.velocity.setMag(mag)

    def collideFront(self):
        index = self.lane.cars.index(self)
        if index == 0:
            return
        otherCar = self.lane.cars[index-1]
        if self.distance(self.pos,otherCar.pos) < 30:
            self.changeVelocity(otherCar.velocity.magnitude)
    def setDirections(self,points):
        pass
        

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    startTime = time.time()
    firstTime = startTime
    intersectionMap = Map()


    lanes = []
    lanes.append(Lane(100,15,'horizontal',1,100,genRate=50))
    lanes.append(Lane(300,15,'horizontal',1,100,genRate=50))
    intersectionMap.addLane(lanes[0])
    intersectionMap.addLane(lanes[1])

    targets = []

    for i in range(5):
        lanes.append(Lane(100+20*i,15,'vertical',1,100,genRate=50))
        intersectionMap.addLane(lanes[-1])
        intersectionMap.addPoint((100+20*i,0),lanes[-1])
        intersectionMap.addPoint((100+20*i,SCREEN_SIZE[0]),lanes[-1])
        targets.append(intersectionMap.graph[-1])
        
    for i in range(5,10):
        lanes.append(Lane(100+20*i,15,'vertical',-1,100,genRate=50))
        intersectionMap.addLane(lanes[-1])
        intersectionMap.addPoint((100+20*i,0),lanes[-1])
        intersectionMap.addPoint((100+20*i,SCREEN_SIZE[0]),lanes[-1])
        targets.append(intersectionMap.graph[-2])

        
    intersectionMap.addPoint((SCREEN_SIZE[0],100),lanes[0])
    intersectionMap.addPoint((SCREEN_SIZE[1],300),lanes[1])
    targets.append(intersectionMap.graph[-1])
    targets.append(intersectionMap.graph[-2])




    while True:
        screen.fill(WHITE)
        for l in lanes:
            for car in l.cars:
                if not len(car.directions):
                    car.directions = intersectionMap.bfs(random.choice(targets))
                elif l == lanes[5]:
                    for p in car.directions:p.render(screen)

        deltaTime = time.time() - startTime
        startTime = time.time()
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for l in range(len(lanes)):
            lanes[l].renderLines(screen)
            lanes[l].update(deltaTime,firstTime)
            for carA in lanes[l].cars:
                carA.velocity.setMag(lanes[l].speedLimit)
                for otherLane in range(len(lanes)):
                    
                    if otherLane == carA:continue
                    for carB in lanes[otherLane].cars:
                        carA.willCollide(carB)
                    
                carA.collideFront()
        for l in lanes:
            l.cleanOut()
            l.renderCars(screen)
            
        pygame.display.update()
