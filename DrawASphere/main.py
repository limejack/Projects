import pygame,sys,math
from pygame.locals import *



class Vector():
    def __init__(self,lis):
        self.vec = lis
        self.pointer = 0
        self.mag = math.sqrt(sum(i**2 for i in lis))
    def magnitude(self):
        return self.mag
    def __add__(self,other):
        return Vector([i[0]+i[1] for i in zip(self,other)])
    def __iter__(self):
        self.pointer = 0
        return self
    def __len__(self):
        return len(self.vec)
    def __next__(self):
        self.pointer += 1
        if self.pointer <= len(self):
            return self.vec[self.pointer-1]
        raise StopIteration
    def __str__(self):
        return str(self.vec)
    def __sub__(self,other):
        return self + (-1*other)
    def __mul__(self,other):
        return Vector([other*i for i in self])
    def __rmul__(self,other):
        return self*other
    def __truediv__(self,other):
        return self*(1/other)
    def __getitem__(self,other):
        return self.vec[other]
    def cross(self,other):
        if len(other) == 3:
            return Vector([self.vec[1]*other.vec[2]-self.vec[2]*other.vec[1],-(self.vec[0]*other.vec[2]-self.vec[2]*other.vec[0]),self.vec[0]*other.vec[1]-self.vec[1]*other.vec[0]])
    def dot(self,other):
        return sum(self.vec[i]*other.vec[i] for i in range(len(self.vec)))
class Tri():
    def __init__(self,points):
        self.points = points
    def draw(self,screen,projection,color):
        pygame.draw.polygon(screen,(color,color,color),[[self.points[j].pos[i] for i in projection] for j in range(3)])
    def isFacing(self,other):
        normal = (self.points[1].pos-self.points[0].pos).cross(self.points[2].pos-self.points[0].pos)
        return normal.dot(other) >= 0
    def getLighting(self,lightSource):
        normal = -1*(self.points[1].pos-self.points[0].pos).cross(self.points[2].pos-self.points[0].pos)
        normal = normal/normal.mag
        midpoint = Vector([sum(self.points[i].pos[j] for i in range(3)) for j in range(3)])/3
        vec = lightSource-midpoint
        vec = vec/vec.mag
        #pygame.draw.line(screen,(255,0,0),(midpoint[1],midpoint[2]),(lightSource[1],lightSource[2]))
        return max(0,normal.dot(vec)*255)

class Point():
    def __init__(self,pos):
        self.pos = pos
def rotate(point,angle):
    out = [point[0]*math.cos(angle)+point[1]*math.sin(angle),-point[0]*math.sin(angle)+point[1]*math.cos(angle)]
    return Vector(out+[point[2]])
def project(point,center,radius):
    p = point-center
    p = p/p.magnitude()
    return p+center
def triangulate(triangle):
    A = Point((triangle.points[0].pos-triangle.points[1].pos)/2+triangle.points[1].pos)
    B = Point((triangle.points[1].pos-triangle.points[2].pos)/2+triangle.points[2].pos)
    C = Point((triangle.points[2].pos-triangle.points[0].pos)/2+triangle.points[0].pos)
    return [Tri([triangle.points[0],A,C]),Tri([triangle.points[1],B,A]),Tri([triangle.points[2],C,B]),Tri([A,B,C])]

def draw(tris,screen):
    newTris = []
    for i in tris:
        temp = Tri(i.points[:])
        newTris.append(temp)
        for j in range(len(i.points)):
            p = temp.points[j]
            temp.points[j] = Point(p.pos*100+Vector([0,250,250]))

    tris = newTris
    toDraw = []
    for i in tris:
        if i.isFacing(Vector([1,0,0])):
           toDraw.append(i)
    lightSource = Vector([-500,500,250])
    for i in toDraw:
        color = i.getLighting(lightSource)
        i.draw(screen,Vector([1,2]),color)
        #pygame.draw.line(screen,(0,0,255),(i.points[0].pos[1],i.points[0].pos[2]),(i.points[1].pos[1],i.points[1].pos[2]))
        #pygame.draw.line(screen,(0,0,255),(i.points[2].pos[1],i.points[2].pos[2]),(i.points[1].pos[1],i.points[1].pos[2]))
        #pygame.draw.line(screen,(0,0,255),(i.points[2].pos[1],i.points[2].pos[2]),(i.points[0].pos[1],i.points[0].pos[2]))

def rotateAll(tris,dt):
    pointsDone = set()
    for i in tris:
        for j in i.points:
            if j not in pointsDone:
                j.pos = rotate(j.pos,dt)
                pointsDone.add(j)
screen = pygame.display.set_mode((500,500))
dimensions = (500,500)
center = dimensions[0]/2,dimensions[1]/2
screen.fill((255,255,255))

tris = []
height = math.sqrt(3)/2
icosohedron = []
frontier = []
points = []
for i in range(5):
    temp = Vector([0,1,0])
    points.append(Point(rotate(temp,math.pi*2/5*i)))
    points[-1].pos = points[-1].pos - Vector([0,0,height/2])

for i in range(5):
    temp = Vector([0,1,0])
    points.append(Point(rotate(temp,math.pi*2/5*(i+0.5))))
    points[-1].pos = points[-1].pos + Vector([0,0,height/2])
for i in range(4):
    tris.append(Tri([points[i],points[i+1],points[i+5]]))
tris.append(Tri([points[4],points[0],points[9]]))
for i in range(4):
    tris.append(Tri([points[i+6],points[i+5],points[i+1]]))
tris.append(Tri([points[5],points[9],points[0]]))

points.append(Point(Vector([0,0,-height/2])))
points.append(Point(Vector([0,0,height/2])))

for i in range(4):
    tris.append(Tri([points[i+1],points[i],points[-2]]))
tris.append(Tri([points[0],points[4],points[-2]]))
for i in range(4):
    tris.append(Tri([points[i+5],points[i+6],points[-1]]))
tris.append(Tri([points[9],points[5],points[-1]]))

temp = []

    

for i in tris:
    for p in i.points:
        p.pos = project(p.pos,Vector([0,0,0]),1)

for i in range(1):
    newTris = []
    for j in tris:
        newTris += triangulate(j)
    tris = newTris


for i in tris:
    for p in i.points:
        p.pos = project(p.pos,Vector([0,0,0]),1)






while True:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    rotateAll(tris,0.01)
    draw(tris,screen)
    pygame.display.update()
