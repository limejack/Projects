def miniMax(moves):
    return Max_Value(board,turn,moves,5,-math.inf,math.inf,0,turn)
def Max_Value(board, color,moves, max_depth, a, b, depth,start):
    if depth >= max_depth or checkIsWonBot(board):
        x = ('Final',(evaluate(board,start),(-1,-1)))
        return x[1]
    v = (-math.inf,(-1,-1))

    for move in moves:
        board[move[0]][move[1]] = color
        temp = Min_Value(board,'x' if color == 'o' else 'o',possible_moves(board,'x' if color == 'o' else 'o',move),max_depth,a,b,depth+1,start)
        board[move[0]][move[1]] = '.'
        v = max(v,(temp[0],move))
        if v[0] > b:
            return v
        a = max(a,v[0])
    return v

def Min_Value(board, color,moves, max_depth, a, b, depth,start):
    if depth >= max_depth or checkIsWonBot(board):
        return (evaluate(board,start),(-1,-1))
    v = (math.inf,(-1,-1))

    for move in moves:
        board[move[0]][move[1]] = color
        temp = Max_Value(board,'x' if color == 'o' else 'o',possible_moves(board,'x' if color == 'o' else 'o',move),max_depth,a,b,depth+1,start)
        board[move[0]][move[1]] = '.'
        v = min(v,(temp[0],move))
        if v[0] < a:
            return v
        b = min(b,v[0])
    return v
def evaluate(board,color):
    out = 0
    for i in range(3):
        for j in range(3):
            won = checkWin(board,(i,j))
            if won == color:
                out += 1000
            elif won and won != 't':
                out -= 500
            box = (i,j)
            for b in toCheckForWin:
                toParse = []
                for a in b:
                    
                    if board[a[0]+3*box[0]][a[1]+3*box[1]] != '.':
                        toParse.append(board[a[0]+3*box[0]][a[1]+3*box[1]])
                if len(toParse) == 2 and toParse[0] == toParse[1]:
                    out += 20*(-1 if toParse[0] != color else 1)

                
    won = checkIsWonBot(board)
    if won == color:
        return math.inf
    if won != color and won:
        return -math.inf
    
    return out
def drawGrid(screen):
    for line in range(9):
        pygame.draw.line(screen,(0,0,0),(0,500/9 * line),(500,500/9 * line))
    for line in range(9):
        pygame.draw.line(screen,(0,0,0),(500/9 * line,0),(500/9 * line,500))
def drawBiggerLines():
    for line in range(1,4):
        pygame.draw.line(screen,(0,0,0),(0,500/3 * line),(500,500/3 * line),5)
    for line in range(1,4):
        pygame.draw.line(screen,(0,0,0),(500/3 * line,0),(500/3 * line,500),5)

def genboard():
    board = []
    for i in range(9):
        temp = '.'*9
        board.append(list(temp))
    return board

def possible_moves(board,color,last_move):
    moves = []
    if last_move == (-1,-1):
        return [(3,3),(3,4),(3,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)]
    nextBox = (last_move[0]%3,last_move[1]%3)
    outs = []
    boardsWon = []
    for i in range(3):
        for j in range(3):
            if checkWin(board,(i,j)):
                boardsWon.append((i,j))
    if nextBox in boardsWon:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == '.' and (i//3,j//3) not in boardsWon:
                    outs.append((i,j))
    else:
        for i in range(nextBox[0]*3,nextBox[0]*3+3):
            for j in range(nextBox[1]*3,nextBox[1]*3+3):
                if board[i][j] == '.' and (i//3,j//3) not in boardsWon:
                    outs.append((i,j))
    return outs
def checkIsWonBot(board):
    boardsWon = {}
    for i in range(3):
        for j in range(3):
            x = checkWin(board,(i,j))
            if x:
                boardsWon[(i,j)] = x
    return checkFinal(boardsWon)
def checkWin(board,box):
    o = 0
    for i in toCheckForWin:
        toParse = []
        for j in i:
            if board[j[0]+3*box[0]][j[1]+3*box[1]] != '.':
                toParse.append(board[j[0]+3*box[0]][j[1]+3*box[1]])
        if len(toParse) == 3 and toParse[0] == toParse[1] == toParse[2]:
            return toParse[0]
        elif len(toParse) == 3:
            o += 1
    if o == len(toCheckForWin):
        return 't'
def checkFinal(won):
    o = 0
    for i in toCheckForWin:
        toParse = []
        for j in i:
            if j in won:
                toParse.append(won[j])
        if len(toParse) == 3 and toParse[0] == toParse[1] == toParse[2] and toParse[0] != 't':
            return toParse[0]
        elif len(toParse) == 3:
            o += 1
    if o == len(toCheckForWin):
        return 't'

def drawMoves(moves):
    for move in moves:
        pygame.draw.rect(screen,(0,255,0),(move[0]*500/9,move[1]*500/9,500/9+1,500/9+1))

def drawBoard(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'x':
                pygame.draw.line(screen,(0,0,0),(i*500/9,j*500/9),((i+1)*500/9,(j+1)*500/9))
                pygame.draw.line(screen,(0,0,0),((i+1)*500/9,j*500/9),((i)*500/9,(j+1)*500/9))
            elif board[i][j] == 'o':
                pygame.draw.circle(screen,(0,0,0),(((i+0.5)*500/9),((j+0.5)*500/9)),0.5*500/9,1)
def drawWon(won):
    for i in won:
        pygame.draw.rect(screen,(255,255,255),(i[0]*500/3,i[1]*500/3,500/3+1,500/3+1))
        if won[i] == 'x':
            pygame.draw.line(screen,(0,0,0),(i[0]*500/3,i[1]*500/3),((i[0]+1)*500/3,(i[1]+1)*500/3))
            pygame.draw.line(screen,(0,0,0),((i[0]+1)*500/3,i[1]*500/3),(i[0]*500/3,(i[1]+1)*500/3))
        elif won[i] == 'o':
            pygame.draw.circle(screen,(0,0,0),(((i[0]+0.5)*500/3),((i[1]+0.5)*500/3)),0.5*500/3,1)

def randomPlayer():
    return random.choice(currentMoves)
import sys, pygame,random,math
from pygame.locals import *
pygame.font.init()
scene = 'opening'
toCheckForWin = [[(0,0),(0,1),(0,2)],
                 [(1,0),(1,1),(1,2)],
                 [(2,0),(2,1),(2,2)],
                 [(0,0),(1,0),(2,0)],
                 [(0,1),(1,1),(2,1)],
                 [(0,2),(1,2),(2,2)],
                 [(0,0),(1,1),(2,2)],
                 [(0,2),(1,1),(2,0)]]
board = genboard()
turn = 'x'
index = {'x':0,'o':1}
currentMoves = possible_moves(board,turn,(-1,-1))
boardsWon = {}
font = pygame.font.SysFont(None, 24)
textToPut = {'p':'Human','r':'Random','c':'CPU'}
victor = None
while True:
    if scene == 'play':
        screen.fill((255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                moveClicked = (int(event.pos[0]//(500/9)),int(event.pos[1]//(500/9)))
                if moveClicked in currentMoves and players[index[turn]] == 'p':
                    board[moveClicked[0]][moveClicked[1]] = turn
                    temp = checkWin(board,(moveClicked[0]//3,moveClicked[1]//3))
                    if temp:
                        boardsWon[(moveClicked[0]//3,moveClicked[1]//3)] = temp
                    if turn == 'x':
                        turn = 'o'
                    else:
                        turn = 'x'
                    currentMoves = possible_moves(board,turn,moveClicked)
                    victor = checkFinal(boardsWon)
                    if victor:
                        scene = 'won'
        drawMoves(currentMoves)
        drawBoard(board)
        drawGrid(screen)
        drawWon(boardsWon)
        drawBiggerLines()
        if turn == 'x':
            pygame.draw.rect(screen,(0,0,0),(0,500,250,50))
            screen.blit(p1Text[1],(10,525))
            screen.blit(p2Text[0],(300,525))
        else:
            pygame.draw.rect(screen,(0,0,0),(250,500,250,50))
            screen.blit(p1Text[0],(10,525))
            screen.blit(p2Text[1],(300,525))

        pygame.display.update()

        if players[index[turn]] == 'r':
            move = randomPlayer()
            board[move[0]][move[1]] = turn
            if checkWin(board,(move[0]//3,move[1]//3)):
                boardsWon[(move[0]//3,move[1]//3)] = turn
            if turn == 'x':
                turn = 'o'
            else:
                turn = 'x'
            currentMoves = possible_moves(board,turn,move)
            victor = checkFinal(boardsWon)
            if victor:
                scene = 'won'
        elif players[index[turn]] == 'c':
            temp = miniMax(currentMoves)
            move = temp[1]
            print(temp)
            print()
            board[move[0]][move[1]] = turn
            if checkWin(board,(move[0]//3,move[1]//3)):
                boardsWon[(move[0]//3,move[1]//3)] = turn
            if turn == 'x':
                turn = 'o'
            else:
                turn = 'x'
            currentMoves = possible_moves(board,turn,move)
            victor = checkFinal(boardsWon)
            if victor:
                scene = 'won'
    elif scene == 'won':
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        drawBoard(board)
        drawGrid(screen)
        drawWon(boardsWon)
        drawBiggerLines()
        if victor == 'x':
            screen.blit(finalText[0],(200,525))
        else:
            screen.blit(finalText[1],(200,525))
        pygame.display.update()
    elif scene == 'opening':
        players = (input('Player 1: '),input('Player 2: '))
        screen = pygame.display.set_mode((500,550))
        p1Text = [font.render('Player 1: '+textToPut[players[0]], True, (0,0,0)),font.render('Player 1: '+textToPut[players[0]], True, (255,255,255))]
        p2Text = [font.render('Player 2: '+textToPut[players[1]], True, (0,0,0)),font.render('Player 1: '+textToPut[players[0]], True, (255,255,255))]
        finalText = [font.render('Player 1 VICTORY('+textToPut[players[0]]+')',True,(0,0,0)),font.render('Player 2 VICTORY('+textToPut[players[1]]+')',True,(0,0,0))]
        scene = 'play'
