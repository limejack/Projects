import pyautogui,time
import cv2 as cv
import numpy as np

def getArray(img_name):
    img = cv.imread(img_name)
    kernel = np.ones((5, 5), np.uint8)

    #cv.imwrite("shot.jpg",img)
    jump = 182
    colleges = []
    colorValues   = []
    for i in range(4):
        tempCollege = []
        tempColors = []
        for j in range(4):
            top = (20+i*jump,20+j*jump)
            bottom = (int(745/4)-5+i*jump,int(750/4)-5+j*jump)
            colors = getColors(img,top,bottom)
            topColors = get2MostCommon(colors)
            tempColors.append(topColors)
            tempCollege.append(getCollege(topColors))
        colleges.append(tempCollege)
        colorValues.append(tempColors)
#    for i in range(4):
 #       for j in range(4):
  #          print(colleges[j][i],end="\t")
   #     print()
##    for j in range(4):
##        for i in range(4):
##            print(colorValues[j][i],end="\t\t")
##        print()

    return colleges

    

def roundColor(pixel):
    pixel = (pixel[2],pixel[1],pixel[0])
    colors = [(193,192,191),(255,255,255),(207,108,39),(135,53,60),(60,87,70)]
    color = (0,0,0)
    minDist = 255*3
    for i in colors:
        dist = distanceToColor(pixel,i)
        if dist < minDist:
            color = i
            minDist = dist
    return color
    
def distanceToColor(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])
def get2MostCommon(colors):
    mostCommon = []
    for i in colors:
        if len(mostCommon) < 2:
            mostCommon.append((colors[i],i))
            continue
        minColor = min(a[0] for a in mostCommon)
        if colors[i] > minColor:
            for j in range(len(mostCommon)):
                if mostCommon[j][0] == minColor:
                    mostCommon[j] = (colors[i],i)
                    break
    return [i[1] for i in mostCommon]
def getCollege(colors):
    baseColors = [(193,192,191),(255,255,255),(207,108,39),(135,53,60),(60,87,70)]  
    colleges = [(0,3),(1,2),(3,4)]
    actualColors = [baseColors.index(i) for i in colors]

    if len(actualColors) < 2:
        return 0
    
    for c in colleges:
        if c and actualColors[0] in c and actualColors[1] in c: return colleges.index(c)
    return -1
    
def getColors(img,top,bottom):
    colors = {}
    for i in range(top[0],bottom[0],3):
        for j in range(top[1],bottom[1],3):
            pixel = roundColor(tuple(img[i,j]))
            if pixel in colors:
                colors[pixel] += 1
            else:
                colors[pixel] = 1
    return colors
def collegeArrayToArray(array):
    out = []
    for i in array:
        temp = []
        for j in i:
            if j != -1 and j != 0:
                temp.append(2**j)
            elif j == -1:
                temp.append(0)
            else:   
                temp.append(0)
        out.append(temp)
    return out
def updateBoard(array,board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                board[i][j] = array[i][j]
    return board
import gameWinner
if __name__ == "__main__":

    directions = ['up','down','left','right']
    time.sleep(1)

    board = gameWinner.createBoard()
    while True:
        time.sleep(0.1)
        img = pyautogui.screenshot(region=(255,514, 745, 750))
        img.save("base.jpg")

#        array = getArray("base.jpg")
#        gameWinner.showBoard(array)
#        break
        baseArray = getArray("base.jpg")
        array = collegeArrayToArray(baseArray)
        board = updateBoard(array,board)
        
        gameWinner.showBoard(board)
  
        
        move = gameWinner.getMove(board)
        board = gameWinner.makeMove(move,board)
        #gameWinner.showBoard(board)
        print(gameWinner.printMove(move))
        pyautogui.press(directions[move])
        

        time.sleep(0.5)
