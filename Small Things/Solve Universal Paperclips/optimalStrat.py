from phaseTheFirst import *

class Node():
    def __init__(self,time,market_level,numClipper,clips,cash,price,total):
        self.time = time
        self.market_level = market_level
        self.numClipper = numClipper
        self.clips = clips
        self.cash = cash
        self.price = price
        self.total = total
        

if __name__ == '__main__':
    frontier = [Node(0,3,24,0,0,getOptimalPrice(getMarketing(3),1,3,24),0)]

    out = []

    maxTime = 30
    longestTime = 0

    while frontier:
        current = frontier.pop(0)
        if current.time > maxTime:
            out.append(current)
            continue
        if current.time >longestTime:
            print(current.time)
            longestTime = current.time
        current.time += 1

        marketing = getMarketing(current.market_level)
        dc,dm = simulate(1,marketing,1,3,current.price,current.numClipper)
        current.cash += dm
        current.clips += dc

        clipperCost = getClipperCost(current.numClipper)
        temp = Node(current.time,current.market_level,current.numClipper,current.clips,current.cash,current.price,current.numClipper)
        while temp.cash < clipperCost:
            temp.time += 1
            dc,dm = simulate(1,getMarketing(temp.market_level),1,3,temp.price,temp.numClipper)
            temp.total += dc
            temp.clips += dc
            temp.cash += dm
        temp.cash -= getClipperCost(temp.numClipper)
        temp.numClipper += 1
        temp.price = getOptimalPrice(getMarketing(temp.market_level),1,3,temp.numClipper)
        frontier.append(temp)

        temp = Node(current.time,current.market_level,current.numClipper,current.clips,current.cash,current.price,current.numClipper)
        while temp.cash < temp.market_level*100:
            temp.time += 1
            dc,dm = simulate(1,getMarketing(temp.market_level),1,3,temp.price,temp.numClipper)
            temp.total += dc
            temp.clips += dc
            temp.cash += dm
        temp.cash -= temp.market_level*100
        temp.market_level += 1
        temp.price = getOptimalPrice(getMarketing(current.market_level+1),1,3,current.numClipper)
        frontier.append(temp)
