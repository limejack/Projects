import re
from urllib.request import urlopen

def readURL(url):
    return urlopen(url).read().decode('utf-8')


def readFromFile():
    out = []
    total = 0
    with open('mappedColors.txt') as inFile:
        for line in inFile.readlines():
            lineParsed = re.match('(\(.*?\)) (.*)',line)
            color = eval(lineParsed[1])
            number =  int(lineParsed[2])
            out.append((number,)+color)
            total += number
    return out,total
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


if __name__ == '__main__':
    colorList,total = readFromFile()
    colorList = sorted(colorList)[::-1]
    ctn,ntc,actualColors = pullColors()

    
    for i in range(min(10,len(colorList))):
        print(f'{int(colorList[i][0]/total*1000)/10} percent: ',ctn[colorList[i][1:]])
