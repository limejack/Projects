def getNeighbors():
    with open('Neighbors.txt') as infile:
        return eval(infile.read())
def getHousesInCounty(county):
    with open(county) as infile:
        return [eval(i) for i in infile.read().split('\n')[:-1]]
def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
def getBorders(pointsA,pointsB):
    border = []
    for i in pointsA:
        for j in pointsB:
            if dist(i,j) < 10:
                border.append(i)
    return border
if __name__ == '__main__':
    neighbors = getNeighbors()
    counties = list(neighbors.keys())

    borders = {}
    for i in range(len(counties)):
        print(counties[i])
        currentNeighbors = neighbors[counties[i]]
        currentSpots = getHousesInCounty(counties[i])
        currentBorder = []
        borders[counties[i]] = []
        for j in currentNeighbors:
            points = getHousesInCounty(j)
            borders[counties[i]] += getBorders(currentSpots,points)
        print('Done')
    with open('borders.txt','w') as outfile:
        outfile.write(str(borders))
