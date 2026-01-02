import random,math,re

def readFromFile():
    colorList = {}
    with open('mappedColors.txt') as inFile:
        for line in inFile.readlines():
            lineParsed = re.match('(\(.*?\)) (.*)',line)
            color = eval(lineParsed[1])
            number =  int(lineParsed[2])
            colorList[color] = number
    return colorList

def sortByMeans(k_means,colors):
    out = [[] for i in range(len(k_means))]

    for c in colors:
        minDist = math.inf
        minMean = 0

        for i in range(len(k_means)):
            d = dist(k_means[i],c)
            if d < minDist:
                minMean = i
                minDist = d

        out[minMean].append((c,colors[c]))
    return out

def dist(colorA,colorB):
    out = 0
    for i in range(3):
        out += (colorA[i]-colorB[i])**2
    return math.sqrt(out)
def calcMean(lis):
    R = 0
    G = 0
    B = 0

    t = 0
    
    for i,n in lis:
        R += i[0]*n
        G += i[1]*n
        B += i[2]*n
        t += n

    if t == 0:
        return -1
    return (R/t,G/t,B/t)

def generateRandomColor():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def getMeans(k):
    k_means = [generateRandomColor() for i in range(k)]

    previousMeans = k_means[:]

    colors = readFromFile()
    while True:
        sortedMeans = sortByMeans(k_means,colors)
        newMeans = [calcMean(mean) for mean in sortedMeans]
        if -1 in newMeans:
            k_means = [generateRandomColor() for i in range(k)]
            continue

        previousMeans = k_means[:]
        k_means = newMeans[:]

        diff = 0
        for i in range(k):
            diff += abs(previousMeans[i][0]-k_means[i][0])
            diff += abs(previousMeans[i][1]-k_means[i][1])
            diff += abs(previousMeans[i][2]-k_means[i][2])
        if diff == 0:
            break

    nums = sortByMeans(k_means,colors)
    
    return k_means,[sum(j[1] for j in i) for i in nums]
    

if __name__ == '__main__':
    k = 3
    print(f'{k} means')

    print(getMeans(k))
