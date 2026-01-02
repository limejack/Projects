import random,math
def pushLeft(board):
    out = []
    for i in board:
        out.append(i[:])

    merged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for x in range(1,len(board[0])):
        for y in range(len(board)):
            if out[y][x] == 0:continue
            currentX = x
            while currentX != 0 and out[y][currentX-1] == 0:
                out[y][currentX-1] = out[y][currentX]
                out[y][currentX] = 0
                currentX -= 1
            if currentX != 0 and out[y][currentX-1] == out[y][currentX] and not merged[y][currentX-1]:
                out[y][currentX-1] = 2*out[y][currentX-1]
                out[y][currentX] = 0
                merged[y][currentX-1] = 1
    return out
def pushRight(board):
    out = []
    for i in board:
        out.append(i[:])

    merged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for x in reversed(range(3)):
        for y in range(len(board)):
            if out[y][x] == 0:continue

            currentX = x
            while currentX != 3 and out[y][currentX+1] == 0:
                out[y][currentX+1] = out[y][currentX]
                out[y][currentX] = 0
                currentX += 1
            
            if currentX != 3 and out[y][currentX+1] == out[y][currentX] and not merged[y][currentX+1]:
                out[y][currentX+1] = 2*out[y][currentX+1]
                out[y][currentX] = 0
                merged[y][currentX+1] = 1

    return out


def pushUp(board):
    out = []
    for i in board:
        out.append(i[:])

    merged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for x in range(len(board[0])):
        for y in range(1,len(board)):
            if out[y][x] == 0:continue
            currentY = y
            while currentY != 0 and out[currentY-1][x] == 0:
                out[currentY-1][x] = out[currentY][x]
                out[currentY][x] = 0
                currentY -= 1

            if currentY != 0 and out[currentY-1][x] == out[currentY][x] and not merged[currentY-1][x]:
                out[currentY-1][x] = 2*out[currentY][x]
                out[currentY][x] = 0
                merged[currentY-1][x] = 1
    return out
def pushDown(board):
    out = []
    for i in board:
        out.append(i[:])

    merged = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for x in range(len(board[0])):
        for y in reversed(range(3)):
            if out[y][x] == 0:continue
            currentY = y
            while currentY != 3 and out[currentY+1][x] == 0:
                out[currentY+1][x] = out[currentY][x]
                out[currentY][x] = 0
                currentY += 1
            if currentY != 3 and out[currentY+1][x] == out[currentY][x] and not merged[currentY+1][x]:
                out[currentY+1][x] = 2*out[currentY][x]
                out[currentY][x] = 0
                merged[currentY+1][x] = 1
    return out
def makeMove(num,board):
    moves = [pushUp,pushDown,pushLeft,pushRight]
    return moves[num](board)

def getNeighbors(board):
    out = []
    for x in range(len(board[0])):
        for y in reversed(range(len(board))):
            if board[y][x] == 0:
                out.append((createCopy(board),2))
                out[-1][0][y][x] = 2
                out.append((createCopy(board),4))
                out[-1][0][y][x] = 4
    return out
  
    
def showBoard(board):
    for i in board:
        for j in i:
            print(j,end='\t')
        print()
def createCopy(board):
    out = []
    return [i[:] for i in board]
def createBoard():
    return [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
def evaluate(board):
    numberOfBlanks = 0
    for x in board:
        for y in x:
            if y == 0:
                numberOfBlanks += 1
##    distMeasure = 0
##    for x in range(4):
##        for y in range(4):
##            distMeasure += board[y][x]*(4-y+4-x)
    return numberOfBlanks
def expectoMax(board,depth):
    if depth == 2:
        return (evaluate(board),-1)
    outs = []
    for move in range(4):
        scores = []
        temp = makeMove(move,board)
        if temp == board:
            outs.append("hello")
            continue

        for n in getNeighbors(temp):
            scores.append((expectoMax(n[0],depth+1)[0],n[1]))

        outs.append(sum(0.9/len(scores)*i[0] if i[1] == 2 else 0.1/len(scores)*i[0] for i in scores))

    impossible = []
    for i in range(len(outs)):
        if outs[i] == "hello":
            outs[i] = -1
            impossible.append(True)
        else:
            impossible.append(False)

    for i in range(len(outs)):
        if outs[i] == max(outs) and not impossible[i]:
            return (outs[i],i)
    return (-math.inf,-1)
    
def getMove(board):
    move = expectoMax(board,0)
    if move[0] == -math.inf:
        return -1
    return move[1]
def printMove(move):
    moves = ['^',"v","<",">"]
    return moves[move]
def addRandom(board):
    temp = createCopy(board)
    x = random.randint(0,3)
    y = random.randint(0,3)
    while temp[y][x] != 0:
        x = random.randint(0,3)
        y = random.randint(0,3)
    if random.random() > 0.9:
        temp[y][x] = 4
    else:
        temp[y][x] = 2
    return temp
    
if __name__ == '__main__':
    board = createBoard()
    board[0][0] = 4
    board[0][1] = 2
    board[2][0] = 2
    showBoard(board)
    print(printMove(getMove(board)))
    
