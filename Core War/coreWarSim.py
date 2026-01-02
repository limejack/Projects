import random
import pygame
from pygame.locals import *
from math import sqrt

MAX_POINTERS = 50

class Core(list):
    def __init__(self,coresize,playerA,playerB):
        super()
        self.cs = coresize
        
        self.pointers = []
        for i in range(coresize):
            self.append(['DAT.F','$0','$0','-1'])

        aStart = random.randint(0,7999)
        bStart = random.randint(0,7999)

        for i in range(len(playerA)):
            self[aStart+i] = playerA[i].split(' ')+['A']
        for i in range(len(playerB)):
            self[bStart+i] = playerB[i].split(' ')+['B']

        self.pointers.append((aStart,'A'))
        self.pointers.append((bStart,'B'))

        self.defaultMods = {'DAT':'f','MOV':'i'}

    def __getitem__(self, indicies):
        return super(Core,self).__getitem__(indicies%self.cs)
    def __setitem__(self, indicies,value):
        super(Core,self).__setitem__(indicies%self.cs,value)
    def tick(core):
        pointers = core.pointers
        CORESIZE = core.cs

        if not len(pointers):
            return
        
        currentSpot,currentTurn = pointers.pop(0)
        currentInstruction = core[currentSpot]
        core[currentSpot][-1] = currentTurn

        opcode = currentInstruction[0]

        addressModeA,numA = splitNumber(currentInstruction[1])
        addressModeB,numB = splitNumber(currentInstruction[2])

        if not numB:
            raise ValueError(numB)
        

        if opcode == 'DAT':
            return
        elif opcode == 'MOV':

            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            if addressModeB == '#':
                core[currentSpot] = source
                core[currentSpot][-1] = currentTurn
            elif addressModeB == '$':
                core[currentSpot+int(numB)] = source
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                core[currentSpot+int(numB)+int(inter[1][1:])] = source
                core[currentSpot+int(numB)+int(inter[1][1:])][-1] = currentTurn
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                core[currentSpot+int(numB)+int(inter[2][1:])] = source
                core[currentSpot+int(numB)+int(inter[2][1:])][-1] = currentTurn
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                core[currentSpot+int(numB)+int(intermediate[1][1:])] = source
                core[currentSpot+int(numB)+int(intermediate[1][1:])][-1] = currentTurn
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                core[currentSpot+int(numB)+int(intermediate[1][1:])] = source
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                core[currentSpot+int(numB)+int(intermediate[2][1:])] = source
                core[currentSpot+int(numB)+int(intermediate[2][1:])][-1] = currentTurn
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                core[currentSpot+int(numB)+int(intermediate[2][1:])] = source
                core[currentSpot+int(numB)+int(intermediate[2][1:])][-1] = currentTurn
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            pointers.append((currentSpot+1,currentTurn))
        elif opcode == 'ADD':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            destination[2] = destination[2][0] + str((int(destination[2][1:])+int(source[1][1:]))%CORESIZE)
            destination[-1] = currentTurn
            pointers.append((currentSpot+1,currentTurn))

            
        elif opcode == 'SUB':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            destination[2] = destination[2][0] + str((int(destination[2][1:])-int(source[1][1:]))%CORESIZE)
            destination[-1] = currentTurn
            pointers.append((currentSpot+1,currentTurn))

            
        elif opcode == 'MUL':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            destination[2] = destination[2][0] + str(int(destination[2][1:])*int(source[1][1:])%CORESIZE)
            destination[-1] = currentTurn
            pointers.append((currentSpot+1,currentTurn))
            
        elif opcode == 'DIV':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            if int(source[1][1:]) == 0:
                pass
            else: destination[2] = destination[2][0] + str((int(destination[2][1:])//int(source[1][1:]))%CORESIZE)

            destination[-1] = currentTurn
            pointers.append((currentSpot+1,currentTurn))
            
        elif opcode == 'MOD':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            if int(source[1][1:]) != 0:
                destination[2] = destination[2][0] + str((int(destination[2][1:])%int(source[1][1:]))%CORESIZE)
            destination[-1] = currentTurn
            pointers.append((currentSpot+1,currentTurn))


        elif opcode == 'JMP':
            if addressModeA == '#':
                dest = currentSpot
            elif addressModeA == '$':
                dest = currentSpot+int(numA)
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
            if addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            if addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
            if addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)


            pointers.append((dest,currentTurn))

            
        elif opcode == 'JMZ':
            if addressModeA == '#':
                dest = currentSpot
            elif addressModeA == '$':
                dest = currentSpot+int(numA)
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)


            if destination[2][1:] == '0':
                pointers.append((dest,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))
        elif opcode == 'JMN':
            if addressModeA == '#':
                dest = currentSpot
            elif addressModeA == '$':
                dest = currentSpot+int(numA)
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)


            if destination[2][1:] != '0':
                pointers.append((dest,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))

        elif opcode == 'DJN':
            if addressModeA == '#':
                dest = currentSpot
            elif addressModeA == '$':
                dest = currentSpot+int(numA)
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)


            destination[2] = destination[2][0]+ str((int(destination[2][1:])-1)%CORESIZE)
            destination[-1] = currentTurn

            if destination[2][1:] != '0':
                pointers.append((dest,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))
        elif opcode == 'SEQ':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            if destination == source:
                pointers.append((currentSpot+2,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))
        elif opcode == 'SNQ':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            if destination != source:
                pointers.append((currentSpot+2,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))
                
        elif opcode == 'SLT':
            if addressModeA == '#':
                source = core[currentSpot][:]
            elif addressModeA == '$':
                source = core[currentSpot+int(numA)][:]
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[1][1:])][:]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                source = core[currentSpot+int(numA)+int(intermediate[2][1:])][:]
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                raise ValueError('Common man')

            
            if addressModeB == '#':
                destination = core[currentSpot]
            elif addressModeB == '$':
                destination = core[currentSpot+int(numB)]
            elif addressModeB == '*':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[1][1:])]
            elif addressModeB == '@':
                inter = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(inter[2][1:])]
            elif addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
            elif addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[1][1:])]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
            elif addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                destination = core[currentSpot+int(numB)+int(intermediate[2][1:])]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)

            if int(destination[2][1:]) > int(source[2][1:]):
                pointers.append((currentSpot+2,currentTurn))
            else:
                pointers.append((currentSpot+1,currentTurn))

        elif opcode == 'SPL':
            if addressModeA == '#':
                dest = currentSpot
            elif addressModeA == '$':
                dest = currentSpot+int(numA)
            elif addressModeA == '*':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '@':
                intermediate = core[currentSpot+int(numA)][:]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '{':
                intermediate = core[currentSpot+int(numA)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
            elif addressModeA == '}':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[1][1:])
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            elif addressModeA == '<':
                intermediate = core[currentSpot+int(numA)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
            elif addressModeA == '>':
                intermediate = core[currentSpot+int(numA)]
                dest = currentSpot+int(numA)+int(intermediate[2][1:])
                intermediate[1] = intermediate[2][0]+str(int(intermediate[2][1:])+1)
            else:
                print(addressModeA)
                raise ValueError('Common man')

            
            if addressModeB == '{':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])-1)
            if addressModeB == '}':
                intermediate = core[currentSpot+int(numB)]
                intermediate[1] = intermediate[1][0]+str(int(intermediate[1][1:])+1)
            if addressModeB == '<':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])-1)
            if addressModeB == '>':
                intermediate = core[currentSpot+int(numB)]
                intermediate[2] = intermediate[2][0]+str(int(intermediate[2][1:])+1)


            pointers.append((currentSpot+1,currentTurn))

            numDone = 0
            for i in pointers:
                if i[1] == currentTurn:
                    numDone += 1
            if numDone < MAX_POINTERS:
                pointers.append((dest,currentTurn))

        Alive = False
        Blive = False
        for i in pointers:
            if i[1] == 'A':
                Alive = True
            elif i[1] == 'B':
                Blive = True
        if Alive and Blive:
            return False
        elif Alive:
            return 'A'
        elif Blive:
            return 'B'

    def draw(self,screen,w,h):
        screen.fill((255,255,255))
        totalArea = w*h
        boxSize = sqrt(totalArea//self.cs)
        numW    = w//boxSize+1


        
        for i in range(self.cs):
            x = i%numW*boxSize
            y = i//numW*boxSize

            if self[i][-1] == 'A':
                pygame.draw.rect(screen,(255,0,0),(x,y,boxSize,boxSize))
            elif self[i][-1] == 'B':
                pygame.draw.rect(screen,(0,0,255),(x,y,boxSize,boxSize))
            if i == self.pointers[0][0]:
                pygame.draw.rect(screen,(0,0,0),(x,y,boxSize,boxSize),1)
                


def splitNumber(num):
    if num[0] in '0123456789':
        return '$',num
    return num[0],num[1:]



if __name__ == '__main__':
    core = Core(8000,['ADD #1 $3','DJN $-1 $1','DAT.F #0 $4','DAT.F #0 $0'],[])
