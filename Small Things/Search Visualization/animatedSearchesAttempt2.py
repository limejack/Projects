class DFS():
    def __init__(self,maze,start):
        self.maze = maze
        self.frontier = [start]
        self.parents = {start:'S'}
        self.explored = set()
        self.done = False
        self.current = start
    def render(self,screen,pos):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                pygame.draw.rect(screen,colors[self.maze[x][y]],(x*(size[0]/width)+pos*size[0],y*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.explored:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        path = [self.current]
        while path[-1] != 'S':
            path.append(self.parents[path[-1]])
        path.pop()
        for p in path:
            pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
       

    def tick(self):
        current = self.frontier.pop()
        self.explored.add(current)

        if maze[current[0]][current[1]] == 'G':
            self.done = True
            return True
        children = []
        children.append((current[0]-1,current[1])) #Walls stop overflow
        children.append((current[0]+1,current[1]))
        children.append((current[0],current[1]+1))
        children.append((current[0],current[1]-1))

        for child in children:
            if maze[child[0]][child[1]] != '#' and child not in self.explored:
                self.frontier.append(child)
                self.parents[child] = current
        self.current = current

        return False
class BFS():
    def __init__(self,maze,start):
        self.maze = maze
        self.frontier = [start]
        self.parents = {start:'S'}
        self.explored = set()
        self.done = False
        self.current = start
    def render(self,screen,pos):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                pygame.draw.rect(screen,colors[self.maze[x][y]],(x*(size[0]/width)+pos*size[0],y*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.explored:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        path = [self.current]
        while path[-1] != 'S':
            path.append(self.parents[path[-1]])
        path.pop()
        for p in path:
            pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
       

    def tick(self):
        current = self.frontier.pop(0)
        self.explored.add(current)

        if maze[current[0]][current[1]] == 'G':
            self.done = True
            return True
        children = []
        children.append((current[0]-1,current[1])) #Walls stop overflow
        children.append((current[0]+1,current[1]))
        children.append((current[0],current[1]+1))
        children.append((current[0],current[1]-1))

        for child in children:
            if maze[child[0]][child[1]] != '#' and child not in self.explored:
                self.frontier.append(child)
                self.parents[child] = current
        self.current = current

        return False
class DoubleBFS():
    def __init__(self,maze,start):
        self.maze = maze
        goal = self.findGoal()

        self.frontierA = [start]
        self.frontierB = [goal]
        self.parentsA = {start:'S'}
        self.parentsB = {goal:'G'}
        self.exploredA = set()
        self.exploredB = set()
        self.done = False
        self.currentA = start
        self.currentB = goal
        self.whichEnd = 1
        
    def findGoal(self):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y] == 'G':
                    return (x,y)
        raise ValueError("No goal")

    def render(self,screen,pos):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                pygame.draw.rect(screen,colors[self.maze[x][y]],(x*(size[0]/width)+pos*size[0],y*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.exploredA:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.exploredB:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        if not self.done:
            path = [self.currentA]
            while path[-1] != 'S':
                path.append(self.parentsA[path[-1]])
            path.pop()
            for p in path:
                pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
            path = [self.currentB]
            while path[-1] != 'G':
                path.append(self.parentsB[path[-1]])
            path.pop()
            for p in path:
                pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
        else:
            if self.currentA in self.exploredB:
                path = [self.currentA]
                while path[-1] != 'S':
                    path.append(self.parentsA[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
                path = path[::-1]
                while path[-1] != 'G':
                    path.append(self.parentsB[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
            elif self.currentB in self.exploredA:
                path = [self.currentB]
                while path[-1] != 'G':
                    path.append(self.parentsB[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
                path = path[::-1]
                while path[-1] != 'S':
                    path.append(self.parentsA[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))

            else:
                raise ValueError("Some weired result happened")

    def tick(self):
        if self.whichEnd %2 == 0:
            current = self.frontierA.pop(0)
            self.exploredA.add(current)

            if maze[current[0]][current[1]] == 'G':
                self.done = True
                return True
            if current in self.exploredB:
                self.currentA = current
                self.done = True
                return True

            children = []
            children.append((current[0]-1,current[1])) #Walls stop overflow
            children.append((current[0]+1,current[1]))
            children.append((current[0],current[1]+1))
            children.append((current[0],current[1]-1))

            for child in children:
                if maze[child[0]][child[1]] != '#' and child not in self.exploredA:
                    self.frontierA.append(child)
                    self.parentsA[child] = current
            self.currentA = current
        else:
            current = self.frontierB.pop(0)
            self.exploredB.add(current)

            if maze[current[0]][current[1]] == 'S':
                self.done = True
                return True
            if current in self.exploredA:
                self.currentB = current
                self.done = True
                return True
            children = []
            children.append((current[0]-1,current[1])) #Walls stop overflow
            children.append((current[0]+1,current[1]))
            children.append((current[0],current[1]+1))
            children.append((current[0],current[1]-1))

            for child in children:
                if maze[child[0]][child[1]] != '#' and child not in self.exploredB:
                    self.frontierB.append(child)
                    self.parentsB[child] = current
            self.currentB = current
        self.whichEnd += 1

        return False
                
class Astar():
    def __init__(self,maze,start):
        self.maze = maze
        self.frontier = [(self.h(start),start,0)]
        self.parents = {start:'S'}
        self.explored = set()
        self.done = False
        self.current = start
        goal = self.findGoal()
    def findGoal(self):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y] == 'G':
                    return (x,y)
        raise ValueError("No goal")
    def render(self,screen,pos):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                pygame.draw.rect(screen,colors[self.maze[x][y]],(x*(size[0]/width)+pos*size[0],y*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.explored:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        path = [self.current]
        while path[-1] != 'S':
            path.append(self.parents[path[-1]])
        path.pop()
        for p in path:
            pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
       
    def h(self,pos):
        return (abs(goal[0]-pos[0])+abs(goal[1]-pos[1]))*10
    def tick(self):
        temp = heapq.heappop(self.frontier)
        current = temp[1]
        self.explored.add(current)

        if maze[current[0]][current[1]] == 'G':
            self.done = True
            return True
        children = []
        children.append((current[0]-1,current[1])) #Walls stop overflow
        children.append((current[0]+1,current[1]))
        children.append((current[0],current[1]+1))
        children.append((current[0],current[1]-1))

        for child in children:
            if maze[child[0]][child[1]] != '#' and child not in self.explored:
                heapq.heappush(self.frontier,(temp[-1]+self.h(child),child,temp[-1]+1))
                self.parents[child] = current
        self.current = current

        return False


class DoubleAstar():
    def __init__(self,maze,start):
        self.maze = maze
        goal = self.findGoal()
        self.frontierA = [(self.h(start,goal),start,0)]
        self.frontierB = [(self.h(start,start),goal,0)]
        self.parentsA = {start:'S'}
        self.parentsB = {goal:'G'}
        self.exploredA = set()
        self.exploredB = set()
        self.done = False
        self.currentA = start
        self.currentB = goal
        self.goal = goal
        self.start = start
        self.whichOne = 0
    def findGoal(self):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y] == 'G':
                    return (x,y)
        raise ValueError("No goal")
    def render(self,screen,pos):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                pygame.draw.rect(screen,colors[self.maze[x][y]],(x*(size[0]/width)+pos*size[0],y*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.exploredA:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        for ex in self.exploredB:
            pygame.draw.rect(screen,colors['*'],(ex[0]*(size[0]/width)+pos*size[0],ex[1]*(size[1]/height),size[0]/width,size[1]/height))
        if not self.done:
            path = [self.currentA]
            while path[-1] != 'S':
                path.append(self.parentsA[path[-1]])
            path.pop()
            for p in path:
                pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
            path = [self.currentB]
            while path[-1] != 'G':
                path.append(self.parentsB[path[-1]])
            path.pop()
            for p in path:
                pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
        else:
            if self.currentA in self.exploredB:
                path = [self.currentA]
                while path[-1] != 'S':
                    path.append(self.parentsA[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
                path = path[::-1]
                while path[-1] != 'G':
                    path.append(self.parentsB[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
            elif self.currentB in self.exploredA:
                path = [self.currentB]
                while path[-1] != 'G':
                    path.append(self.parentsB[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))
                path = path[::-1]
                while path[-1] != 'S':
                    path.append(self.parentsA[path[-1]])
                path.pop()
                for p in path:
                    pygame.draw.rect(screen,colors['-'],(p[0]*(size[0]/width)+pos*size[0],p[1]*(size[1]/height),size[0]/width,size[1]/height))

            else:
                raise ValueError("Some weired result happened")
       
    def h(self,pos,goal):
        return (abs(goal[0]-pos[0])+abs(goal[1]-pos[1]))*10
    def tick(self):
        if self.whichOne %2== 0:
            temp = heapq.heappop(self.frontierA)
            current = temp[1]
            self.exploredA.add(current)

            if maze[current[0]][current[1]] == 'G':
                self.done = True
                return True
            if current in self.exploredB:
                self.currentA = current
                self.done = True
                return True

            children = []
            children.append((current[0]-1,current[1])) #Walls stop overflow
            children.append((current[0]+1,current[1]))
            children.append((current[0],current[1]+1))
            children.append((current[0],current[1]-1))

            for child in children:
                if maze[child[0]][child[1]] != '#' and child not in self.exploredA:
                    heapq.heappush(self.frontierA,(temp[-1]+self.h(child,self.goal),child,temp[-1]+1))
                    self.parentsA[child] = current
            self.currentA = current



        else:
            temp = heapq.heappop(self.frontierB)
            current = temp[1]
            self.exploredB.add(current)

            if maze[current[0]][current[1]] == 'S':
                self.done = True
                return True
            if current in self.exploredA:
                self.currentB = current
                self.done = True
                return True
            children = []
            children.append((current[0]-1,current[1])) #Walls stop overflow
            children.append((current[0]+1,current[1]))
            children.append((current[0],current[1]+1))
            children.append((current[0],current[1]-1))

            for child in children:
                if maze[child[0]][child[1]] != '#' and child not in self.exploredB:
                    heapq.heappush(self.frontierB,(temp[-1]+self.h(child,self.start),child,temp[-1]+1))
                    self.parentsB[child] = current
            self.currentB = current
            
        self.whichOne += 1
        return False

def generateGoal(maze):
    goalX = random.randint(0,49)
    goalY = random.randint(0,49)
    while maze[goalX][goalY] == '#':
        goalX = random.randint(0,49)
        goalY = random.randint(0,49)
    return (goalX,goalY)


import pygame, mazeMaker
from pygame.locals import *
import random,time,sys,heapq

colors = {'.':(255,255,255),'#':(0,0,0),'G':(255, 0, 0),'*':(245, 213, 242),'-':(119, 217, 247)}

maze = mazeMaker.generateMaze(50,50,meathod='prim')

goal = generateGoal(maze)
#goal = (49,49)
#while maze[goal[0]][goal[1]] == '#':
#    goal = (goal[0],goal[1]-1)
#    if goal[1] < 0:
#        goal = (goal[0]-1,49)

maze[goal[0]][goal[1]] = 'G'
#start = generateGoal(maze) #ahem this should not be used like this but im lazy
start = (0,0)
while maze[start[0]][start[1]] == '#':
    start = (start[0],start[1]+1)
    if start[1] > 49:
        start = (start[0]+1,0)

searches = [BFS(maze,start),Astar(maze,start),DFS(maze,start),DoubleAstar(maze,start)]


startTime = time.time()
textSize = 15
height = 50
width = 50
size = (300,300)
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((size[0]*len(searches),size[1]+textSize*2),RESIZABLE)

font = pygame.font.SysFont('arial',textSize)
texts = []
textRects = []
for i in range(len(searches)):
    texts.append(font.render('hi',True,(0,0,0),(255,255,255)))
    textRects.append(texts[-1].get_rect())
    textRects[-1].center = (size[0]*(1+2*i)/2,size[1]+textSize)


while True:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    for i in range(len(texts)): screen.blit(texts[i],textRects[i])
    for s in enumerate(searches):
        s[1].render(screen,s[0])
        if s[1].done: continue

        s[1].tick()

        t = -1*(startTime-time.time())
        min = str(int(t//60))
        sec = str(int(t%60))
        texts[s[0]] = font.render(f'{("0" if not len(min)-1 else "")+min}:{("0" if not len(sec)-1 else "")+sec}',True,(0,0,0),(255,255,255))

    clock.tick(10)
    pygame.display.update()
