def chooseA(board):
    return board[0]
def Random(board):
    return random.choice(board)
def chooseB(board):
    return board[1]
    
def simGame(a,b,n,board):
    scoreA = 0
    scoreB = 0
    for i in range(n):
        dA,dB = a(b(board))
        scoreA += dA
        scoreB += dB
    return (scoreA,scoreB)

import random


if __name__ == '__main__':
    board = [[(2,2),(2,9)],[(9,2),(10,10)]]
    N = 10000
    strats = [chooseA,Random,chooseB]
    
    scores = {}
    for i in strats:
        scores[i] = 0

        
    for i in strats:
        for j in strats:
            points = simGame(i,j,N,board)
            scores[i] += points[0]
            scores[j] += points[1]

    x = strats[0]
    for i in strats:
        if scores[i] > scores[x]:
            x = i
    print(x)
