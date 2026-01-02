def numSoldPerSec(demand):
    #return 0.7*demand**(2.15)/10
    if demand/100 > 1:
        return 0.7*(demand**1.15)*10
    else:
        return 0.7*demand**(2.15)/10
        
def getDemand(clipPrice,marketing,marketingEffectivness,UNI_NUMBER):
    return 0.8/clipPrice*marketing*marketingEffectivness*(1+0.1*(UNI_NUMBER-1))
def getMarketing(level):
    return 1.1**(level-1)
def getClipsMadePerSec(numClippers,numMega):
    return numClippers*7.5+500*numMega*2.75
def simulate(time,marketing,marketingEffectivness,UNI_NUMBER,price,numClippers,numMega):
    clipsMadePerSec = getClipsMadePerSec(numClippers,numMega)
    clips = 0
    money = 0
    for i in range(time):
        demand = getDemand(price,marketing,marketingEffectivness,UNI_NUMBER)
        clips += clipsMadePerSec
        sold = numSoldPerSec(demand)
        if sold > clips:
            money += clips*price
            clips = 0
        else:
            clips -= sold
            money += sold*price
    return clips,money
def getOptimalPrice(marketing,marketingEffectivness,UNI_NUMBER,numClippers,numMega):
    clipsMadePerSec = getClipsMadePerSec(numClippers,numMega)
    for i in range(1,100):
        price = i/100
        demand = getDemand(price,marketing,marketingEffectivness,UNI_NUMBER)
        clipsSold = numSoldPerSec(demand)
        if clipsSold < clipsMadePerSec:
            return i/100
def getClipperCost(numClippers):
    return 1.1**(numClippers)+5
if __name__ == '__main__':
    UNI_NUMBER = 3
    numClippers = 83
    numMega = 73
    marketing_level = 17
    marketingEffectivness = 15
    marketing = getMarketing(marketing_level)

    clips = 0
    money = 0

    maxCash = 0
    maxClips = 0
    maxVals = (0,0)
    for i in range(1,100):
        for j in range(1,100):
            clips,money = simulate(10,marketing,marketingEffectivness,UNI_NUMBER,i/100,numClippers,numMega)
            dc,dm = simulate(10,marketing,marketingEffectivness,UNI_NUMBER,j/100,numClippers,numMega)
            if money + dm > maxCash:
                maxCash = money+dm
                maxClips = clips + dc
                maxVals = (i,j)
    print('Values',maxVals)
    print(maxCash,maxClips)

    clips,money = simulate(20,marketing,marketingEffectivness,UNI_NUMBER,getOptimalPrice(marketing,marketingEffectivness,UNI_NUMBER,numClippers,numMega),numClippers,numMega)
    print(money,clips)
    print(getOptimalPrice(marketing,marketingEffectivness,UNI_NUMBER,numClippers,numMega))
