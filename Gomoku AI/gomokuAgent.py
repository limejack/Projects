import random,math,sys
import pygame
from pygame.locals import *

class Line():
    def __init__(self,color,start,end,length):
        self.start = start
        self.end = end
        self.color = color
        self.length = length
    def __len__(self):
        return self.length
    def __str__(self):
        return 'Length: '+str(self.length)+" Start: "+str(self.start)+" End: "+str(self.end)
class Row(Line):
    def isFree(self,board):
        freeSpaces = 0
        if board.getTile(self.start[0]-1,self.start[1]) == '.':
            freeSpaces += 1
        if board.getTile(self.end[0]+1,self.end[1]) == '.':
            freeSpaces += 1
        return freeSpaces
class Column(Line):
    def isFree(self,board):
        freeSpaces = 0
        if board.getTile(self.start[0],self.start[1]-1) == '.':
            freeSpaces += 1
        if board.getTile(self.end[0],self.end[1]+1) == '.':
            freeSpaces += 1
        return freeSpaces
class Diagonal1(Line):
    def isFree(self,board):
        freeSpaces = 0
        if board.getTile(self.start[0]-1,self.start[1]-1) == '.':
            freeSpaces += 1
        if board.getTile(self.end[0]+1,self.end[1]+1) == '.':
            freeSpaces += 1
        return freeSpaces
class Diagonal2(Line):
    def isFree(self,board):
        freeSpaces = 0
        if board.getTile(self.start[0]+1,self.start[1]-1) == '.':
            freeSpaces += 1
        if board.getTile(self.end[0]-1,self.end[1]+1) == '.':
            freeSpaces += 1
        return freeSpaces

            
class RandomAgent():
    def __init__(self,color):
        self.color = color

    def getMove(self,board,moveCounter):
        x = random.randint(0,board.width-1)
        y = random.randint(0,board.height-1)

        while board[y][x] != '.':
            x = random.randint(0,board.width-1)
            y = random.randint(0,board.height-1)

        return (x,y)
class HumanAgent():
    def __init__(self,color):
        self.color = color

        pygame.init()
        self.screen = pygame.display.set_mode((500,500))

        self.screen.fill((255,255,255))
        pygame.display.update()

    def getMove(self,board,moveCounter):

        blockWidth = 500//board.width
        blockHeight = 500//board.height

        
        self.drawGrid(self.screen,board)
        self.renderBoard(board,self.screen,blockWidth,blockHeight)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    pos = event.pos
                    x = pos[0]//blockWidth
                    y = pos[1]//blockHeight

                    if board[y][x] != '.':
                        continue
                    return(x,y)
                    
        return (x,y)
    def renderBoard(self,board,screen,blockWidth,blockHeight):
        colors = {'W':1,'B':0}
        for x in range(len(board[0])):
            for y in range(len(board)):
                if board[y][x] != '.':
                    pygame.draw.circle(screen,(0,0,0),(blockWidth*x+blockWidth/2,blockHeight*y+blockHeight/2),blockWidth/2,colors[board[y][x]])

        
    def drawGrid(self,screen,board):
        blockWidthX = 500//board.width
        for x in range(board.width):
            pygame.draw.line(screen,(0,0,0),(x*blockWidthX,0),(x*blockWidthX,500))
        for y in range(board.height):
            pygame.draw.line(screen,(0,0,0),(0,y*(500//board.height)),(500,y*(500//board.height)))



class MinMaxAgent():
    def __init__(self,color):
        self.color = color
        self.depth = 3
        self.range = 1
        self.colorSwitch = {'B':'W','W':'B'}

    def getMove(self,board,moveCounter):            
        return self.maxFunction(board,moveCounter,0,-math.inf,math.inf)[0]

    def minFunction(self,board,moveCounter,depth,alpha,beta):
        
        if depth > self.depth or moveCounter >= board.width*board.height:
            return (0,0),self.evaluate(board,self.colorSwitch[self.color])
        hasWon = board.checkWin()
        if hasWon == self.color:
            return (0,0),math.inf
        elif hasWon == self.colorSwitch[self.color]:
            return (0,0),-math.inf

        minScore = math.inf
        minMove  = None
        color = self.colorSwitch[self.color]


        for move in self.getMoves(board,self.colorSwitch[self.color]):
            if minMove == None:minMove = move
            board.makeMove(move,color)
            score = self.maxFunction(board,moveCounter+1,depth+1,alpha,beta)[1]
            board.makeMove(move,'.')
            if minScore > score:
                minMove = move
                minScore = score
            if minScore <= alpha:
                break
            beta = min(beta,minScore) 

        return minMove,minScore


    def maxFunction(self,board,moveCounter,depth,alpha,beta):
        if depth > self.depth or moveCounter >= board.width*board.height or board.checkWin():
            return (0,0),self.evaluate(board,self.color)

        hasWon = board.checkWin()
        if hasWon == self.color:
            return (0,0),math.inf
        elif hasWon == self.colorSwitch[self.color]:
            return (0,0),-math.inf


        maxScore = -math.inf
        maxMove  = None

        for move in self.getMoves(board,self.color):
            if maxMove == None:maxMove = move
            board.makeMove(move,self.color)
            score = self.minFunction(board,moveCounter+1,depth+1,alpha,beta)[1]
            board.makeMove(move,'.')

            if maxScore < score:
                maxMove = move
                maxScore = score
            if maxScore >= beta:
                break
            alpha = max(alpha,maxScore)
        if depth == 0:
            print(maxScore)
        return maxMove,maxScore

    def getMoves(self,board,color):
        output = set()
        if board.empty:
            return [(board.width//2,board.height//2)]
            
        for x in range(board.width):
            for y in range(board.height):
                if board[y][x] != '.':
                    self.lineOfSight(board,x,y,output)
                    
        if not output:
            return {(0,0)}

        finalOut = list(output)
        finalDict = {}

        return finalOut

    def lineOfSight(self,board,x,y,out):
        for i in range(x-self.range,x):
            if board.getTile(i,y) == '.':
                out.add((i,y))
                
        for i in range(y-self.range,y):
            if board.getTile(x,i) == '.':
                out.add((x,i))
                
        for i in range(x+1,x+self.range+1):
            if board.getTile(i,y) == '.':
                out.add((i,y))

        for i in range(y+1,y+self.range+1):
            if board.getTile(x,i) == '.':
                out.add((x,i))

        for i in range(1,self.range+1):
            if board.getTile(x+i,y+i) == '.':
                out.add((x+i,y+i))
            if board.getTile(x-i,y-i) == '.':
                out.add((x-i,y-i))
            if board.getTile(x-i,y+i) == '.':
                out.add((x-i,y+i))
            if board.getTile(x+i,y-i) == '.':
                out.add((x+i,y-i))




    def evaluate(self,board,turn):
        score = 0
        lines = self.grabLines(board)

        if None in lines:
            print(lines)
            print(board)
            raise ValueError("NONE FOUND")

        hasAFour = [False,False]
        
        for i in lines:
            scoreChange = self.gradeLine(i,self.color)

            if len(i) == 4 and i.isFree(board) > 1:
                if i.color == self.color:
                    hasAFour[0] = True
                else:
                    hasAFour[1] = True
            if   len(i) == 4 and i.isFree(board) >= 1 and turn == i.color and i.color == self.color:
                return math.inf
            elif len(i) == 4 and i.isFree(board) >= 1 and i.color == turn and i.color != self.color:
                return -math.inf

            if i.isFree(board) == 0:
                continue
            
            elif i.isFree(board) == 1:
                scoreChange /= 2

            score += scoreChange
        
        return score

    def gradeLine(self,line,color):
        scores = {1:0,2:1,3:3,4:3}
        out = 0
        if len(line) < 5:
            out = scores[len(line)]
        else:
            out = math.inf

        if line.color != color:
            out *= -1

        return out

    def grabLines(self,board):
        rows = self.grabRows(board)
        columns = self.grabColumns(board)
        diags1 = self.grabDiag1(board)
        diags2 = self.grabDiag2(board)
        return rows+columns+diags1+diags2
    def grabDiag1(self,board):
        x = board.width-1
        y = 0

        startX = x
        startY = y
        out = []
        temp = []

        while True:
            if board[y][x] != '.' and len(temp) and board[y][x] == temp[-1]:
                temp.append(board[y][x])
            elif board[y][x] != '.' and len(temp):
                out.append(Diagonal1(temp[-1],(x-len(temp),y-len(temp)),(x-1,y-1),len(temp)))
                temp = [board[y][x]]
            elif board[y][x] != '.' and not len(temp):
                temp = [board[y][x]]
            if board[y][x] == '.' and len(temp):
                out.append(Diagonal1(temp[-1],(x-len(temp),y-len(temp)),(x-1,y-1),len(temp)))
                temp = []
            y += 1
            x += 1
            if x >= board.width or y >= board.height:

                if startX > 0:

                    startX -= 1
                    if len(temp):
                        out.append(Diagonal1(temp[-1],(x-len(temp),y-len(temp)),(x,y),len(temp)))
                        temp = []
                else:
                    startY += 1
                    if startY >= board.height:
                        if len(temp):
                            out.append(Diagonal1(temp[-1],(x-len(temp),y-len(temp)),(x,y),len(temp)))
                        return out
                x = startX
                y = startY

    def grabDiag2(self,board):
        x = 0
        y = 0

        startX = x
        startY = y
        out = []
        temp = []

        while True:
            if board[y][x] != '.' and len(temp) and board[y][x] == temp[-1]:
                temp.append(board[y][x])
            elif board[y][x] != '.' and len(temp):
                out.append(Diagonal2(temp[-1],(x+len(temp),y-len(temp)),(x+1,y-1),len(temp)))
                temp = [board[y][x]]
            elif board[y][x] != '.' and not len(temp):
                temp = [board[y][x]]
            if board[y][x] == '.' and len(temp):
                out.append(Diagonal2(temp[-1],(x+len(temp),y-len(temp)),(x+1,y-1),len(temp)))
                temp = []
            y += 1
            x -= 1
            if x < 0 or y >= board.height:

                if startX < board.width-1:

                    startX += 1
                    if len(temp):
                        out.append(Diagonal2(temp[-1],(x+len(temp),y-len(temp)),(x+1,y-1),len(temp)))
                        temp = []
                else:
                    startY += 1
                    if y >= board.height:
                        if len(temp):
                            out.append(Diagonal2(temp[-1],(x+len(temp),y-len(temp)),(x,y),len(temp)))
                        return out
                x = startX
                y = startY


        
    def grabColumns(self,board):
        columns = []
        x = 0
        y = 0
        temp = []

        while True:
            if board[y][x] != '.' and len(temp) and board[y][x] == temp[-1]:
                temp.append(board[y][x])
            elif board[y][x] != '.' and len(temp):
                columns.append(Column(temp[-1],(x,y-len(temp)),(x,y-1),len(temp)))
                temp = [board[y][x]]
            elif board[y][x] != '.' and not len(temp):
                temp = [board[y][x]]
            if board[y][x] == '.' and len(temp):
                columns.append(Column(temp[-1],(x,y-len(temp)),(x,y-1),len(temp)))
                temp = []

            y += 1
            if y >= board.height:
                y = 0
                x += 1
                if len(temp):
                    columns.append(Column(temp[-1],(x,y-len(temp)),(x,y),len(temp)))
                    temp = []
            if x >= board.width:
                if len(temp):
                    columns.append(Column(temp[-1],(x,y-len(temp)),(x,y),len(temp)))
                    temp = []
                return columns


    def grabRows(self,board):
        rows = []
        x = 0
        y = 0
        temp = []

        while True:
            if board[y][x] != '.' and len(temp) and board[y][x] == temp[-1]:
                temp.append(board[y][x])
            elif board[y][x] != '.' and len(temp):
                rows.append(Row(temp[-1],(x-len(temp),y),(x-1,y),len(temp)))
                temp = [board[y][x]]
            elif board[y][x] != '.' and not len(temp):
                temp = [board[y][x]]
            if board[y][x] == '.' and len(temp):
                rows.append(Row(temp[-1],(x-len(temp),y),(x-1,y),len(temp)))

                temp = []

            x += 1
            if x >= board.width:
                x = 0
                y += 1

                if len(temp):
                    rows.append(Row(temp[-1],(x-len(temp),y),(x,y),len(temp)))
                    temp = []

            if y >= board.height:
                if len(temp):
                    rows.append(rows.append(Row(temp[-1],(x-len(temp),y),(x,y),len(temp))))
                return rows






        
class Board(list):
    def __init__(self,height,width):
        super()
        self.height = height
        self.width  = width
        for y in range(height):
            temp = []
            for x in range(width):
                temp.append('.')
            self.append(temp)
        self.empty = True
    def __str__(self):
        lines = []
        for line in self:
            lines.append(''.join(line))
        return '\n'.join(lines)
            
    def getTile(self,x,y):
        if x < self.width and x >= 0 and y < self.height and y >= 0:
            return self[y][x]
        return None
        
    def checkWin(self):
        for y in range(self.height):
            for x in range(self.width):
                temp = self.checkSpace(x,y)
                if temp:return temp

    def checkSpace(self,x,y):
        a = self.checkRow(x,y)            
        if a: return a
        b = self.checkColumn(x,y)            
        if b: return b
        c = self.checkDiag(x,y)            
        if c: return c
        
    def makeMove(self,move,color):
        self[move[1]][move[0]] = color
        self.empty = False
        
    def checkRow(self,x,y):
        if self.width - x -1< 5:
            return None
        if self[y][x] == '.':return

        tempX = x
        counter = 0
        while self[y][tempX] == self[y][x]:
            counter += 1
            tempX += 1
        if counter >= 5:
            return self[y][x]
    def checkColumn(self,x,y):
        if self.height - y -1< 5:
            return None
        if self[y][x] == '.':return

        tempY = y
        counter = 0
        while self[tempY][x] == self[y][x]:
            counter += 1
            tempY += 1
        if counter >= 5:
            return self[y][x]
    def checkDiag(self,x,y):
        if self.height - y-1 < 5:
            return None
        if self.width - x-1 < 5:
            return None
        if self[y][x] == '.':return
        tempX = x
        tempY = y
        counter = 0
        while self[tempY][tempX] == self[y][x]:
            counter += 1
            tempX += 1
            tempY += 1
        if counter >= 5:
            return self[y][x]

        if self.height - y-1 < 5:
            return None
        if self.width - x-1 < 5:
            return None
        if self[y][x] == '.':return
        tempX = x
        tempY = y
        counter = 0
        while self[tempY][tempX] == self[y][x]:
            counter += 1
            tempX -= 1
            tempY += 1
        if counter >= 5:
            return self[y][x]


    def getAdjacent(self,x,y):
        outs = []
        if x > 0 and y > 0:
            outs.append((x-1,y-1))
        if y < self.height-1 and x < self.width-1:
            outs.append((x+1,y+1))
        if x > 0:
            outs.append((x-1,y))
        if y > 0:
            outs.append((x,y-1))
        if x < self.width-1:
            outs.append((x+1,y))
        if y < self.height-1:
            outs.append((x,y+1))

        if x > 0 and y < self.height-1:
            outs.append((x-1,y+1))
        if y > 0 and x < self.width-1:
            outs.append((x+1,y-1))
        return outs

if __name__ == '__main__':
    board = Board(13,13)
    a = MinMaxAgent('B')

    board.makeMove((6,6),'B')
    board.makeMove((5,6),'B')
    board.makeMove((4,6),'B')
    board.makeMove((3,6),'B')

    print(board)
    print(a.evaluate(board))
