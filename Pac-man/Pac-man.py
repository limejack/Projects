import pygame, time
from pygame.locals import *
def swap(n1,n2,l):
    l[n1],l[n2] = l[n2],l[n1]
    return l
def resetDots(blockSize,topSpace):
    dots = set()

    for x in range(1,13):
        dots.add((x*blockSize,1*blockSize+topSpace*blockSize))
    for x in range(15,27):
        dots.add((x*blockSize,1*blockSize+topSpace*blockSize))
    for x in range(1,27):
        dots.add((x*blockSize,5*blockSize+topSpace*blockSize))
    for x in range(1,7):
        dots.add((x*blockSize,8*blockSize+topSpace*blockSize))
    for x in range(9,13):
        dots.add((x*blockSize,8*blockSize+topSpace*blockSize))
    for x in range(15,19):
        dots.add((x*blockSize,8*blockSize+topSpace*blockSize))
    for x in range(22,27):
        dots.add((x*blockSize,8*blockSize+topSpace*blockSize))
    for x in range(1,13):
        dots.add((x*blockSize,20*blockSize+topSpace*blockSize))
    for x in range(15,27):
        dots.add((x*blockSize,20*blockSize+topSpace*blockSize))
    for x in range(1,4):
        dots.add((x*blockSize,23*blockSize+topSpace*blockSize))
    for x in range(6,22):
        dots.add((x*blockSize,23*blockSize+topSpace*blockSize))
    for x in range(24,27):
        dots.add((x*blockSize,23*blockSize+topSpace*blockSize))
    for x in range(1,7):
        dots.add((x*blockSize,26*blockSize+topSpace*blockSize))
    for x in range(9,13):
        dots.add((x*blockSize,26*blockSize+topSpace*blockSize))
    for x in range(15,19):
        dots.add((x*blockSize,26*blockSize+topSpace*blockSize))
    for x in range(21,27):
        dots.add((x*blockSize,26*blockSize+topSpace*blockSize))
    for x in range(1,27):
        dots.add((x*blockSize,29*blockSize+topSpace*blockSize))
    for y in range(1,9):
        dots.add((1*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(1,27):
        dots.add((6*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(1,6):
        dots.add((12*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(5,9):
        dots.add((9*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(5,9):
        dots.add((18*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(1,27):
        dots.add((21*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(1,9):
        dots.add((26*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(20,24):
        dots.add((1*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(26,30):
        dots.add((1*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(20,24):
        dots.add((26*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(26,30):
        dots.add((26*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(23,27):
        dots.add((3*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(26,30):
        dots.add((12*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(23,27):
        dots.add((9*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(20,24):
        dots.add((12*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(20,24):
        dots.add((15*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(23,26):
        dots.add((18*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(26,30):
        dots.add((15*blockSize,y*blockSize+topSpace*blockSize))
    for y in range(23,27):
        dots.add((24*blockSize,y*blockSize+topSpace*blockSize))


    return dots

    
def main():
    pygame.init()

    topSpace = 2
    bottomSpace = 4

    blockSize = 10

    dot = pygame.image.load('dot.png')
    
    size = (28*blockSize,31*blockSize)
    screen = pygame.display.set_mode((size[0],topSpace*blockSize+size[1]+bottomSpace*blockSize))

    maze = pygame.image.load('maze.png')
    maze = pygame.transform.scale(maze,size)

    pacSprite = [pygame.image.load('Pac-man1.png'),pygame.image.load('Pac-man2.png'),pygame.image.load('Pac-man3.png'),pygame.image.load('Pac-man2.png')]
    for i in range(len(pacSprite)):
        pacSprite[i] = pygame.transform.scale(pacSprite[i],(blockSize, blockSize))
    pacSprite = [pacSprite]
    for i in range(4):
        pacSprite.append([pygame.transform.rotate(pac,90*i) for pac in pacSprite[0]])
    pacSprite.pop(0)
    swap(3,2,pacSprite)
    swap(1,3,pacSprite)
    startTime = time.time()
    lastTime = startTime
    
    animationPause = 0.1
    speed = 11*blockSize
    pacSpeed = 0.8*speed
    
    pX,pY = (13*blockSize+blockSize/2,23*blockSize + blockSize*topSpace)

    pacDirection = 0
    dList =     [(1,0),(-1,0),(0,1),(0,-1)]
    opposites = [K_LEFT,K_RIGHT,K_UP,K_DOWN]
    directionsDict = {K_UP:3,K_DOWN:2,K_LEFT:1,K_RIGHT:0}

    rows = 31
    columns = 28

    pre = None

    nodesRaw = {(210,230):{K_UP,K_DOWN,K_LEFT},(210,260):{K_UP,K_RIGHT},(260,290):{K_UP,K_LEFT},(210,200):{K_UP,K_DOWN,K_LEFT,K_RIGHT},(240,260):{K_UP,K_LEFT,K_RIGHT},
             (240,230):{K_DOWN,K_RIGHT},(260,230):{K_UP,K_LEFT},(260,200):{K_LEFT,K_DOWN},(260,260):{K_LEFT,K_DOWN},(150,290):{K_UP,K_LEFT,K_RIGHT},(150,260):{K_DOWN,K_RIGHT},
             (180,260):{K_UP,K_LEFT},(180,230):{K_DOWN,K_LEFT,K_RIGHT},(150,200):{K_DOWN,K_RIGHT},(150,230):{K_UP,K_LEFT,K_RIGHT},
             (180,200):{K_UP,K_LEFT,K_RIGHT},(180,170):{K_DOWN,K_LEFT,K_UP},(180,140):{K_UP,K_DOWN,K_RIGHT},(210,140):{K_UP,K_DOWN,K_LEFT,K_RIGHT},
             (180,80):{K_LEFT,K_DOWN},(150,80):{K_DOWN,K_RIGHT},(180,80):{K_UP,K_LEFT},(150,110):{K_UP,K_RIGHT,K_LEFT},(180,110):{K_LEFT,K_DOWN},
             (210,80):{K_UP,K_RIGHT,K_DOWN},(180,50):{K_RIGHT,K_LEFT,K_DOWN},(210,50):{K_UP,K_DOWN,K_LEFT,K_RIGHT},(260,80):{K_LEFT,K_UP},
             (260,50):{K_LEFT,K_DOWN,K_UP},(260,10):{K_DOWN,K_LEFT},(210,10):{K_RIGHT,K_LEFT,K_DOWN},(150,10):{K_DOWN,K_RIGHT},(150,50):{K_UP,K_RIGHT,K_LEFT}}
    nodes = {}
    for node in nodesRaw:
        left,right = False, False
        temp = nodesRaw[node].copy()
        if K_LEFT in temp:
            left = True
        if K_RIGHT in temp:
            right = True
        if left:
            temp.add(K_RIGHT)
            temp.remove(K_LEFT)
        if right:
            temp.add(K_LEFT)
            if not left:
                temp.remove(K_RIGHT)
        nodes[(node[0],node[1]+topSpace*blockSize)] = nodesRaw[node]
        nodes[(135-(node[0]-135),node[1]+topSpace*blockSize)] = temp
        

    
    dots = resetDots(blockSize,topSpace)
    ghosts = [[13.5*blockSize,13*blockSize,1],[13.5*blockSize,13*blockSize,1],[13.5*blockSize,13*blockSize,0]]
    ghostSpeed = 0.75*speed


    ghostSprites = []
    for name in ['Blinky','Pinky','Inky']:
        ghostTemp = []
        for d in ['Right','Left','Down','Up']:
            ghostTemp.append([pygame.image.load(name+d+'1.png'),pygame.image.load(name+d+'2.png')])
        ghostSprites.append(ghostTemp)

        
    for a in ghostSprites:
        for b in a:
            for c in range(len(b)):
                b[c] = pygame.transform.scale(b[c],(blockSize,blockSize))

    score = 0

    lastTurnB = None
    lastTurnP = None
    lastTurnI = None
    preSic = 16
    target = (0,0)
    
    while True:
        screen.blit(maze,(0,topSpace*blockSize))
        #print(pre)
        tx,ty = (pX//(blockSize/preSic))*(blockSize/preSic),(pY//(blockSize/preSic))*(blockSize/preSic)
        bx,by = (ghosts[0][0]//(blockSize/preSic))*(blockSize/preSic),(ghosts[0][1]//(blockSize/preSic))*(blockSize/preSic)
        px,py = (ghosts[1][0]//(blockSize/preSic))*(blockSize/preSic),(ghosts[1][1]//(blockSize/preSic))*(blockSize/preSic)
        ix,iy = (ghosts[2][0]//(blockSize/preSic))*(blockSize/preSic),(ghosts[2][1]//(blockSize/preSic))*(blockSize/preSic)

        if (tx,ty) in [(bx,by),(px,py),(ix,iy)]:
            pygame.quit()
            print('Game Over!')
            return
        
        if tx > 28*blockSize:
            pX,pY = (0,ty)
            tx = 0
        if tx < 0:
            pX = 28*blockSize
            tx = 28*blockSize

        if bx > 28*blockSize:
            ghosts[0] = (0,by,ghosts[0][2])
            bx = 0
        if bx < 0:
            ghosts[0] = (28*blockSize,by,ghosts[0][2])
            bx = 28*blockSize
            
        if px > 28*blockSize:
            ghosts[1] = (0,py,ghosts[1][2])
            px = 0
        if px < 0:
            ghosts[1] = (28*blockSize,py,ghosts[1][2])
            px = 28*blockSize

        if ix > 28*blockSize:
            ghosts[2] = (0,iy,ghosts[2][2])
            ix = 0
        if ix < 0:
            ghosts[2] = (28*blockSize,iy,ghosts[2][2])
            ix = 28*blockSize


        if ((tx,ty) in nodes and pacDirection + 1073741903 in nodes[(tx,ty)]) or (tx,ty) not in nodes:
            pX,pY = (pX+(time.time()-lastTime)*pacSpeed*dList[pacDirection][0],pY+(time.time()-lastTime)*pacSpeed*dList[pacDirection][1])
        if ((bx,by) in nodes and ghosts[0][2] + 1073741903 in nodes[(bx,by)]) or (bx,by) not in nodes:
            if bx < 40 and by == 160 or bx > 210 and by == 160:
                ghosts[0] = (ghosts[0][0]+(time.time()-lastTime)*0.4*speed*dList[ghosts[0][2]][0],ghosts[0][1]+(time.time()-lastTime)*0.4*speed*dList[ghosts[0][2]][1],ghosts[0][2])
            else:
                ghosts[0] = (ghosts[0][0]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[0][2]][0],ghosts[0][1]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[0][2]][1],ghosts[0][2])
        if ((px,py) in nodes and ghosts[1][2] + 1073741903 in nodes[(px,py)]) or (px,py) not in nodes:
            if px < 40 and py == 160 or px > 210 and py == 160:
                ghosts[1] = (ghosts[1][0]+(time.time()-lastTime)*0.4*speed*dList[ghosts[1][2]][0],ghosts[1][1]+(time.time()-lastTime)*0.4*speed*dList[ghosts[1][2]][1],ghosts[1][2])
            else:
                ghosts[1] = (ghosts[1][0]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[1][2]][0],ghosts[1][1]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[1][2]][1],ghosts[1][2])
        if ((ix,iy) in nodes and ghosts[2][2] + 1073741903 in nodes[(ix,iy)]) or (ix,iy) not in nodes:
            if ix < 40 and iy == 160 or ix > 210 and iy == 160:
                ghosts[2] = (ghosts[2][0]+(time.time()-lastTime)*0.4*speed*dList[ghosts[2][2]][0],ghosts[2][1]+(time.time()-lastTime)*0.4*speed*dList[ghosts[2][2]][1],ghosts[2][2])
            else:
                ghosts[2] = (ghosts[2][0]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[2][2]][0],ghosts[2][1]+(time.time()-lastTime)*ghostSpeed*dList[ghosts[2][2]][1],ghosts[2][2])

        if (bx,by) in nodes and lastTurnB != (bx,by):
            temp = []
            for d in nodes[(bx,by)]:
                if d != opposites[ghosts[0][2]]:
                    t = (bx+dList[d-1073741903][0],by+dList[d-1073741903][1],d)
                    temp.append((abs(tx-t[0])+abs(ty-t[1]),)+t)
            ghosts[0] = (ghosts[0][0],ghosts[0][1],min(temp)[3]-1073741903)
            lastTurnB = (bx,by)
        pygame.draw.rect(screen,(255,255,255),(*target,10,10))

        if (px,py) in nodes and lastTurnP != (px,py):
            temp = []
            for d in nodes[(px,py)]:
                if d != opposites[ghosts[1][2]]:
                    t = (px+dList[d-1073741903][0],py+dList[d-1073741903][1],d)
                    temp.append((abs((tx+4*blockSize*dList[pacDirection][0])-t[0])+abs((ty+4**blockSize*dList[pacDirection][1])-t[1]),)+t)
            ghosts[1] = (ghosts[1][0],ghosts[1][1],min(temp)[3]-1073741903)
            lastTurnP = (px,py)
        if (ix,iy) in nodes and lastTurnI != (ix,iy):
            temp = []
            target = ((tx-bx)*2 + bx,(ty-by)*2+by)
            for d in nodes[(ix,iy)]:
                if d != opposites[ghosts[2][2]]:
                    t = (ix+dList[d-1073741903][0],iy+dList[d-1073741903][1],d)
                    temp.append((abs(target[0]-ix)+abs(target[1]-iy),)+t)
            ghosts[2] = (ghosts[2][0],ghosts[2][1],min(temp)[3]-1073741903)
            lastTurnI = (ix,iy)


        lastTime = time.time()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN and (tx,ty) in nodes:
                if event.key == K_DOWN and K_DOWN in nodes[(tx,ty)]:
                    pacDirection = 2
                if event.key == K_UP and K_UP in nodes[(tx,ty)]:
                    pacDirection = 3
                if event.key == K_RIGHT and K_RIGHT in nodes[(tx,ty)]:
                    pacDirection = 0
                if event.key == K_LEFT and K_LEFT in nodes[(tx,ty)]:
                    pacDirection = 1
                pre = None
            elif event.type == KEYDOWN and event.key == opposites[pacDirection]:
                pacDirection = directionsDict[event.key]
                pre = None
            elif event.type == KEYDOWN and event.key in directionsDict: 
               pre = directionsDict[event.key]
            if event.type == MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos()[0]//10,pygame.mouse.get_pos()[1]//10)

        if pre != None and (tx,ty) in nodes and pre+1073741903 in nodes[(tx,ty)]:
            pacDirection = pre
            pre = None


        currentPac = pacSprite[pacDirection][int(((time.time()-startTime)/animationPause)%(len(pacSprite)))]
        currentGhosts = [ghostSprites[0][ghosts[0][2]][int(((time.time()-startTime)/animationPause)%(len(ghostSprites[0][0])))],
                         ghostSprites[1][ghosts[1][2]][int(((time.time()-startTime)/animationPause)%(len(ghostSprites[1][0])))],
                         ghostSprites[2][ghosts[2][2]][int(((time.time()-startTime)/animationPause)%(len(ghostSprites[2][0])))]
                         ]
        

        if (tx,ty) in dots:
            dots.remove((tx,ty))
            score += 10

        for d in dots:
            screen.blit(dot,d)

        #for x in range(rows+1):
        #    pygame.draw.line(screen,(0,255,0),(0,x*((size[1])/rows)),(size[0],x*(size[1])/rows))

        #for x in range(columns+1):
        #    pygame.draw.line(screen,(0,255,0),(x*(size[0]/columns),0),(x*size[0]/columns,size[1]))
        screen.blit(currentGhosts[0],(ghosts[0][0],ghosts[0][1]))
        screen.blit(currentGhosts[1],(ghosts[1][0],ghosts[1][1]))
        screen.blit(currentGhosts[2],(ghosts[2][0],ghosts[2][1]))


        screen.blit(currentPac,(pX,pY))
        pygame.display.update()
        screen.fill((0,0,0))
        
    
if __name__ == '__main__':
    main()
