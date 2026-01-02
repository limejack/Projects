import pandas as pd
import pygame,sys,random
from pygame.locals import *
print("The panda has imported")

def getData():
    data = pd.read_csv('VirginiaSiteAddressPoint.txt',low_memory=False)
    return data
def getSides(data):
    return [36.54213065200002, -83.59094398599996, 39.42581624300004, -75.34102361099998]
    corners = [None,None,None,None] #Left, Top, Bottom, Right

    skipFactor = 10
    skipCounter = 0

    for i in range(0,data.shape[0],100):
        dataPoint = data.loc[i]
        
        if not corners[0] or dataPoint['LAT'] < corners[0]:
            corners[0] = dataPoint['LAT']
        if not corners[1] or dataPoint['LONG'] < corners[1]:
            corners[1] = dataPoint['LONG']
        if not corners[2] or dataPoint['LAT'] > corners[2]:
            corners[2] = dataPoint['LAT']
        if not corners[3] or dataPoint['LONG'] > corners[3]:
            corners[3] = dataPoint['LONG']
    return corners

def offLoad(municipalities):
    for i in municipalities:
        print("Starting "+i)
        file_name = ''.join(i.split())
        file_name = ''.join(i.split('/'))
        with open(file_name+'.txt','w') as outfile:
            for j in municipalities[i]:
                outfile.write(str(j)+'\n')
        print("Finished " + i) 
                
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    screen.fill((255,255,255))

    data = getData()
    print('data loaded')
    sides = getSides(data)
    print('sides loaded')
    colors = {}
    municipalities = {}

    hasOffloaded = False
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        for i in range(10):
            if index > data.shape[0] and not hasOffloaded:
                offLoad(municipalities)
                hasOffloaded = True
                continue
            elif index > data.shape[0]:
                continue
            lat,long = (data.loc[index]['LAT'],data.loc[index]['LONG'])

            x = (lat-sides[0])/(sides[2]-sides[0])*500
            y = (long-sides[1])/(sides[3]-sides[1])*500

            zc = data.loc[index]['MUNICIPALITY']
            if zc in colors:
                color = colors[zc]
                municipalities[zc].append((x,y))
            else:
                colors[zc] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                color = colors[zc]
                municipalities[zc] = []
                municipalities[zc].append((x,y))

            pygame.draw.circle(screen,color,(x,y),1)
            index += 10
        pygame.display.update()
