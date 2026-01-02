def genChild(node,maze,explored,frontier):
    out = []
    if node[0] > 2:
        out.append((node[0]-2,node[1]))
    if node[0] < len(maze)-3:
        out.append((node[0]+2,node[1]))
    if node[1] > 2:
        out.append((node[0],node[1]-2))
    if node[1] < len(maze[0])-3:
        out.append((node[0],node[1]+2))
    return out
def genChildPrim(node,maze):
    out = []
    if node[0] > 1:
        out.append((node[0]-1,node[1]))
    if node[0] < len(maze)-2:
        out.append((node[0]+1,node[1]))
    if node[1] > 1:
        out.append((node[0],node[1]-1))
    if node[1] < len(maze[0])-2:
        out.append((node[0],node[1]+1))
    return out

def printMaze(maze):
    outFile = open(input('Outfile name? '),'w')
    out = []
    for line in enumerate(maze):
        if line[0] == len(maze)-1:
            outFile.write(''.join(line[1]))
        else:
            outFile.write(''.join(line[1])+'\n')
    outFile.close()


def generateMaze(Height,Width,limit=1000,meathod='rdfs'):
    import random

    maze = []
    for x in range(Height):
        temp = []
        for y in range(Width):
            temp.append('#')
        maze.append(temp)

    start = (1,1)
    if meathod == 'rdfs':
        frontier = [start]
        explored = set(start)

        while len(frontier) < limit and len(frontier):
            current = frontier.pop()
            maze[current[0]][current[1]] = '.'
            choices = genChild(current,maze,explored,frontier)
            explored.add(current)
            if len(choices):
                frontier.append(current)
                n = random.choice(choices)
                if n[0]-current[0] == -2:
                    maze[current[0]-1][current[1]] = '.'
                elif n[1]-current[1] == -2:
                    maze[current[0]][current[1]-1] = '.'
                elif n[0]-current[0] == 2:
                    maze[current[0]+1][current[1]] = '.'
                elif n[1]-current[1] == 2:
                    maze[current[0]][current[1]+1] = '.'
                maze[n[0]][n[1]] = '.'
                frontier.append(n)
        return maze
    elif meathod == 'prim':
        wallsList = genChildPrim(start,maze)
        maze[start[0]][start[1]] = '.'
        while len(wallsList):
            current = random.choice(wallsList)
            wallsList.remove(current)
            children = genChildPrim(current,maze)
            symbols = [maze[i[0]][i[1]] for i in children]
            if symbols.count('.') == 1:
                maze[current[0]][current[1]] = '.'
                for child in children:
                    if maze[child[0]][child[1]] == '#':
                        wallsList.append(child)
        return maze
if __name__ == '__main__':
    printMaze(generateMaze(50,50,meathod='prim'))
