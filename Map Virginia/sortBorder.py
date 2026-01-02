def getBorders():
    return eval(open('borders.txt').read())
def getCenter(borders):
    x = sum(i[0] for i in borders)
    y = sum(i[1] for i in borders)

    return x/len(borders),y/len(borders)
def getAngle(point,center):
    return math.atan2(point[1]-center[1],point[0]-center[0])
import math
if __name__ == '__main__':
    borders = getBorders()

    for i in borders:
        print(i)
        county = borders[i]
        center = getCenter(county)
        angles = [(getAngle(county[j],center),j) for j in range(len(county))]
        angles = sorted(angles)
        borders[i] =[county[j[1]] for j in angles]
        print('Done')
    with open('borders.txt','w') as outfile:
        outfile.write(str(borders))
