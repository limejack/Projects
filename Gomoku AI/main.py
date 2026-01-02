from gomokuAgent import *
if __name__ == '__main__':
    agent1 = MinMaxAgent('B')
    agent2 = HumanAgent('W')
    board = Board(13,13)
    moveCounter = 0
    while True:


        #pygame.display.update()
        
        board.makeMove(agent1.getMove(board,moveCounter),agent1.color)
        moveCounter += 1

        print('White:')
        print(board)

        board.makeMove(agent2.getMove(board,moveCounter),agent2.color)
        moveCounter += 1
        winner = board.checkWin()
        if moveCounter >= board.width*board.height:
            print('tie')
            print(board)
            break
        if winner:
            print('Winner! ',winner)
            print(board)
            break
        print('Black:')
        print(board)

        
