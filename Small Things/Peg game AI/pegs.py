class Board():
    def __init__(self):
        self.board = ['..000..',
                      '..000..',
                      '0000000',
                      '000_000',
                      '0000000',
                      '..000..',
                      '..000..']    

    def getMoves(self,x,y):
        moves = [(x-2,y),(x+2,y),(x,y+2),(x,y-2)]
        out = []
    
        for m in moves:
            piece = (int(m[0]/2+x/2),int(m[1]/2+y/2))

    
            if self.getSpace(*m) == '_' and self.getSpace(*piece) == '0':
                out.append(m)
        return out
            

    def getSpace(self,x,y):
        if x < 0 or y < 0 or x >= len(self.board[0]) or y >= len(self.board):
            return '.'
        return self.board[y][x]
    def setTile(self,move,tile):
        self.board[move[1]] = self.board[move[1]][:move[0]] + tile + self.board[move[1]][move[0]+1:]
        

    def makeMove(self,move):
        self.setTile(move[0],'_')
        self.setTile(move[1],'0')

        newMove = (int(move[0][0]/2+move[1][0]/2),
                   int(move[0][1]/2+move[1][1]/2))

        self.setTile(newMove,'_')

    def unmakeMove(self,move):
        self.setTile(move[0],'0')
        self.setTile(move[1],'_')

        newMove = (int(move[0][0]/2+move[1][0]/2),
                   int(move[0][1]/2+move[1][1]/2))

        self.setTile(newMove,'0')

    def display(self):
        for i in self.board: print(i)
    def numPiece(self):
        out = 0
        for line in self.board:
            out += line.count('0')
        return out

        
def recur(board):
    if board.numPiece() < 2:
        board.display()
        print()
        return True
    moves = []
    for x in range(len(board.board[0])):
        for y in range(len(board.board)):
            if board.getSpace(x,y) != '0':
                continue
            m = board.getMoves(x,y)
            for i in m:
                moves.append(((x,y),i))
    for move in moves:
        board.makeMove(move)
        x = recur(board)
        board.unmakeMove(move)

        if x:
            board.display()
            print()
            return True
    return False
    

if __name__ == '__main__':
    board = Board()


    recur(board)
    
