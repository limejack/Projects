class Individual():
    def __init__(self,moves,start):
        self.moves = moves
        self.pos   = start
        self.directions = DIRECTIONS
    def tick(self,k):
        move = self.directions[self.moves[k]]
        self.pos = (self.pos[0]+move[0]*10,self.pos[1]+move[1]*10)
        if self.pos[0] >= SIZE[0] or self.pos[0] < 0 or self.pos[1] < 0 or self.pos[1] >= SIZE[1]: #multiplying checks if either is zero
            self.pos = (self.pos[0]-move[0]*10,self.pos[1]-move[1]*10)
        
    def render(self,screen):
        pygame.draw.rect(screen,RED,(self.pos[0],self.pos[1],10,10))


import pygame,random,time,math
from pygame.locals import *

DIRECTIONS = (((1,0),(0,1),(-1,0),(0,-1),(0,0)))
SIZE = (500,500)
WAITTIME = 0.01
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
FILE  = 'storage.txt'

GOAL  = (490,490)
START = (10,10)

WALLS = []

#Hyperparams
MOVECOUNT = 200
GENSIZE   = 100
MUTATIONRATE = 0.05

def init():
    '''Returns Screen and font, no args
    '''
    #required stuff
    pygame.init()
    pygame.font.init()

    
    screen = pygame.display.set_mode((SIZE[0],SIZE[1]))
    font = pygame.font.Font('freesansbold.ttf', 20)
    return screen,font

def mutate(moves):
    for i in range(len(moves)):
        if random.random() <= MUTATIONRATE:
            moves[i] = random.randint(0,len(DIRECTIONS)-1)

def renderAll(screen,blobs):
    for i in blobs:
        i.render(screen)

def createCreatures():
    out = []
    for i in range(GENSIZE):
        out.append(Individual([random.randint(0,len(DIRECTIONS)-1) for j in range(MOVECOUNT)],START))
    return out

def drawGrid(screen):
    #Only for placing
    for x in range(SIZE[0]//10):
        pygame.draw.line(screen,BLACK,(x*10,0),(x*10,SIZE[1]))
    for y in range(SIZE[1]//10):
        pygame.draw.line(screen,BLACK,(0,y*10),(SIZE[1],y*10))

def drawGoal(screen):
    pygame.draw.rect(screen,BLACK,(*GOAL,10,10))
    
def tickAll(c,k):
    for i in c: i.tick(k)
def pythag(a,b):
    return math.sqrt((a[0]-b[0])**2 + (b[1]-a[1])**2)

def fitness(creature):
    score = -math.log(pythag(creature.pos,GOAL)/400)
    return score
        

def newBatch(creatures):
    probs = {}
    fits =  []
    for creature in creatures:
        fits.append(fitness(creature))
    maxProb = 0
    maxFit = creatures[fits.index(max(fits))]
    maxFit.pos = START

    top5 = [0,1,2,3,4]
    for i in range(5,len(fits)):
        maxs = [fits[i] for i in top5]
        if min(maxs) < fits[i]:
            index = maxs.index(min(maxs))
            top5[index] = i
            
    creatures = [creatures[i] for i in top5]
    fits      = [fits[i]      for i in top5]

    for creature in enumerate(creatures):
        probs[creature[1]] = (maxProb,maxProb+fits[creature[0]]/sum(fits))
        maxProb += fits[creature[0]]/sum(fits)
    outs = []

    for i in range(GENSIZE-1):
        p = random.random()
        parent = None
        for creature in probs:
            if p > probs[creature][0] and p < probs[creature][1]:
                parent = creature

        moves = parent.moves.copy()
        mutate(moves)
        outs.append(Individual(moves,START))
    writeMovesToFile(maxFit.moves)
    return outs+[maxFit]

def clearFile():
    with open(FILE,'w') as file:
        file.write('')
def writeMovesToFile(moves):
    with open(FILE,'a') as file:
        out = list(map(str,moves))
        file.write(''.join(out))
        file.write('\n')
        

def main():
    screen,font = init()
    creatures = createCreatures()
    k = 0
    start = time.time()
    gen = 1
    clearFile()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        screen.fill(WHITE)
        renderAll(screen,creatures)
        drawGoal(screen)
        drawGrid(screen)
        if time.time()-start > WAITTIME and k < MOVECOUNT:
            tickAll(creatures,k)
            k += 1
            start = time.time()
        if k == MOVECOUNT:
            k = 0
            bestPlayer = 1000
            for creature in creatures:
                if pythag(creature.pos,GOAL) < bestPlayer:
                    bestPlayer = pythag(creature.pos,GOAL)
            print(f'Gen {gen}, Best Player :',bestPlayer)
            gen += 1
            creatures = newBatch(creatures)

        pygame.display.update()

if __name__ == '__main__':main()
