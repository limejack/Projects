def tick(startState):
    endState = []
    for x in range(len(startState)):
        temp = []
        for y in range(len(startState[x])):
            temp.append(getTile((x,y),startState))
        endState.append(temp)
    return endState
    
def genAdjs(pos,state):
    out = []
    for i in range(3):
        if i == 0 or i == 1 or pos[0] < len(state)-1 and i == 2:
            for j in range(3):
                if j == 0:
                    out.append((-1+i,-1+j))
                elif j == 1 and i != 1:
                    out.append((-1+i,-1+j))
                elif j == 2 and pos[1] < len(state[0])-1:
                    out.append((-1+i,-1+j))
    
    return out
def getTile(pos,state):
    numBlacks = 0
    for tile in genAdjs(pos,state):
        if state[tile[0]+pos[0]][tile[1]+pos[1]] == 'B':
            numBlacks += 1
    if numBlacks < 2:
        return 'W'
    elif numBlacks in [2,3] and state[pos[0]][pos[1]] == 'B':
        return 'B'
    elif numBlacks > 3:
        return 'W'
    elif numBlacks == 3:
        return 'B'
    return state[pos[0]][pos[1]]

import pygame,sys
from pygame.locals import *
pygame.init()
state = [['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','B','B','B','W','W','W','W','W'],
         ['W','W','W','W','B','W','W','W','W','W'],
         ['W','W','W','B','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],
         ['W','W','W','W','W','W','W','W','W','W'],]
screen = pygame.display.set_mode((200,200))
blockSize = 20
while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            state = tick(state)
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 'B':
                color = (0,0,0)
            else:
                color = (255,255,255)
            pygame.draw.rect(screen,color,(i*blockSize,j*blockSize,blockSize,blockSize))
    pygame.display.update()
