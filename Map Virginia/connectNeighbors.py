import random
class Municipality():
    def __init__(self,name):
        self.name = name
        self.party = random.random()
        self.population = random.randint(100,1000)
class District():
    def __init__(self,start):
        self.counties = [start]
        self.population = start.population
    def getParty(self):
        r_pop = 0
        for i in self.counties:
            r_pop += i.population*i.party
        return int(r_pop > self.population/2)

if __name__ == '__main__':
    with open('Neighbors.txt') as infile:
        neighbors = eval(infile.read())
    counties = []
    districts = []
    for i in neighbors:
        counties.append(Municipality(i))
        districts.append(District(counties[-1]))
