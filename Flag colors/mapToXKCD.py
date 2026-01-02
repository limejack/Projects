from urllib.request import urlopen
import re,math

def readURL(url):
    return urlopen(url).read().decode('utf-8')


def pullColors():
    website_text = readURL('https://www.w3schools.com/colors/colors_xkcd.asp')
    color_hex_name = re.findall('<td>(.*?)</td><td.*?></td><td>(.*?)</td>',website_text)

    color_to_name = {}
    name_to_color = {}
    colors = []

    for color,name in color_hex_name:
        R = int(color[1]+color[2],base=16)
        G = int(color[3]+color[4],base=16)
        B = int(color[5]+color[6],base=16)
        color_to_name[(R,G,B)] = name
        name_to_color[name]    = (R,G,B)
        colors.append((R,G,B))

    return color_to_name,name_to_color,colors

def readFromFile():
    colorList = {}
    with open('colors.txt') as inFile:
        for line in inFile.readlines():
            lineParsed = re.match('(\(.*?\)) (.*)',line)
            color = eval(lineParsed[1])
            number =  int(lineParsed[2])
            colorList[color] = number
    return colorList

def dist(colorA,colorB):
    out = 0
    for i in range(3):
        out += (colorA[i]-colorB[i])**2
    return math.sqrt(out)

def findClosestColor(actualColors,color):
    minDist = math.inf
    minColor = actualColors[0]

    for i in actualColors:
        d = dist(i,color)
        if d < minDist:
            minColor = i
            minDist = d
    return minColor

def mapColorList(actualColors,inColors):
    out = {}
    for i in inColors:
        colorToMap = findClosestColor(actualColors,i)
        if colorToMap in out:
            out[colorToMap] += inColors[i]
        else:
            out[colorToMap] = inColors[i]
    return out

def putInFile(colorsList):
    with open('mappedColors.txt','w') as outFile:
        for i in colorsList:
            outFile.write(str(i)+' '+str(colorsList[i])+'\n')


if __name__ == '__main__':
    rawColorList = readFromFile()
    ctn,ntc,actualColors = pullColors()
    newColorList =  mapColorList(actualColors,rawColorList)
    putInFile(newColorList)
