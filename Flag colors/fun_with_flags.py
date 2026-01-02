from urllib.request import urlopen
import re,io,json
from PIL import Image

def readURL(url):
    return urlopen(url).read().decode('utf-8')

def getFlagColors(url):
    flagData = urlopen('https://'+url).read()
    image_file = io.BytesIO(flagData)
    flag = Image.open(image_file).convert('RGB')
    flag.resize((160,80))
    pix = flag.load()


    colors = {}

    for x in range(flag.size[0]):
        for y in range(flag.size[1]):
            if pix[x,y] in colors:
                colors[pix[x,y]] += 1
            else:
                colors[pix[x,y]] = 1

    return colors
def getCountryNames():
    #json_obj = json.loads(readURL('http://www.geognos.com/api/en/countries/info/all.json'))['Results']
    #countries = []
    #for i in json_obj:
    #    countries.append('http://www.geognos.com/api/en/countries/flag/'+i+'.png')

    countries = []
    text = readURL('https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags')
    urls = re.findall('<img alt=".*?" src="//(upload.wikimedia.org/wikipedia/commons.*?)"',text)
    
    return urls
    
def putInFile(colorsList):
    with open('colors.txt','w') as outFile:
        for i in colorsList:
            outFile.write(str(i)+' '+str(colorsList[i])+'\n')
    
if __name__ == '__main__':
    countryList = getCountryNames()[:-1]
    colorsList = {}
    for i in countryList:
        print(i)
        flagColors = getFlagColors(i)
        for color in flagColors:
            if color not in colorsList:
                colorsList[color] = flagColors[color]
            else:
                colorsList[color] += flagColors[color]
    otherList = {}
    for color in colorsList:
        if colorsList[color] >= 10:
            otherList[color] = colorsList[color]    
        
    putInFile(otherList)
