import pygame,sys,time
from pygame.locals import *
from coreWarSim import Core

def readFile(fileName):
    with open(fileName) as inFile:
        rawData = inFile.read().split('\n')
    out = []
    for i in rawData:
        line = i.split(' ')
        if len(line) == 2:
            line.append('#0')
        if line[1][0] in '-1234567890':
            line[1] = '$'+line[1]
        if line[2][0] in '-1234567890':
            line[2] = '$'+line[2]
        line[0] = line[0].upper()
        out.append(' '.join(line))
    return out

aInstructions = readFile('paper.txt')
bInstructions = ['DJN #2 <-6', 'DJN *5 *5', 'MOV {-6 <1', 'DJN }-5 {0', 'MOD #11 $-8', 'SPL <-11 #3', 'SLT }-5 >-6', 'SLT >7 @1', 'JMN *0 #-6', 'SEQ >3 #4', 'SPL >1 $2']
core = Core(8000,aInstructions,
                 bInstructions)


pygame.init()
screen = pygame.display.set_mode((500,500))

core.draw(screen,500,500)

lastTick = time.time()
lastTock = time.time()

while True:

    if time.time()-lastTick > 0.1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        lastTick = time.time()
        core.draw(screen,500,500)
        pygame.display.update()

    if time.time()-lastTock > 0.01:
        lastTock = time.time()
        won = core.tick()
        if won:
            print(won)

            core.draw(screen,500,500)
            pygame.display.update()
            break

        #for i in core:
            #if i[0] != 'DAT.F':
                #print(i)
        #print('BREAK\n\n\n')
