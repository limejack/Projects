import random
from coreWarSim import Core
commands = ['DAT','MOV','ADD','SUB','MUL','DIV','MOD','JMP','JMZ','JMN','DJN','SEQ','SNQ','SLT','SPL']
address_modes = ['#','$','*','@','{','}','<','>']

MUTATION_RATE = 0.2
MUTATION_SIZE = 5
ADD_SIZE = 1
SUB_SIZE = 1

ADD_RATE = 0.5
SUB_RATE = 0.5

POPULATION = 20
ROUNDS     = 2000
NUM_CLONES = 5
NUM_RANDOM   = 10

class Brain():
    def __init__(self,parent = None,mutate=True):
        if not parent:
            self.instructions = []
            for i in range(random.randint(1,10)):
                self.instructions.append(self.generate_random_instruction())
        else:
            self.instructions = []
            for ins in parent.instructions:
                if random.random() <= MUTATION_RATE:
                    self.instructions.append(self.mutate(ins[:]))
                else:
                    self.instructions.append(ins[:])
            if random.random() <= SUB_RATE:
                self.instructions = self.instructions[:-(random.randint(1,SUB_SIZE))]
            if random.random() <= ADD_RATE:
                for i in range(random.randint(1,ADD_SIZE)):
                    self.instructions.append(self.generate_random_instruction())
            
            
    def generate_random_instruction(self):
        com = random.choice(commands)
        a   = random.choice(address_modes)+str(random.randint(-10,10))
        b   = random.choice(address_modes)+str(random.randint(-10,10))
        return [com,a,b]
    def mutate(self,instruction):
        com = instruction[0]
        if random.random() < MUTATION_RATE * 2:
            com = random.choice(commands)
        a = instruction[1]
        b = instruction[2]

        if random.random() < MUTATION_RATE * 2:
            a = random.choice(address_modes)+a[1:]
            b = random.choice(address_modes)+a[1:]

        if random.random() < 0.5:
            a = a[0]+str(int(a[1:])+random.randint(1,ADD_SIZE))
        else:
            a = a[0]+str(int(a[1:])-random.randint(1,SUB_SIZE))
        if random.random() < 0.5:
            b = b[0]+str(int(b[1:])+random.randint(1,ADD_SIZE))
        else:
            b = b[0]+str(int(b[1:])-random.randint(1,SUB_SIZE))

        return [com,a,b]
    def toStr(self):
        out = []
        for i in self.instructions:
            out.append(' '.join(i))
        return out

def test(a,b):
    testCore = Core(8000,a.toStr(),b.toStr())
    for i in range(10000):
        won = testCore.tick()
        if won:
            return won
    return 'tie'
def playRound(current,toBeat):
    out = []
    for i in current:
        out.append(0)
    for i in range(1):
        for a in range(0,POPULATION):
            for b in range(0,POPULATION):
                winner = test(current[a],current[b])
                if winner == 'A':
                    out[a] += 1
                elif winner == 'B':
                    out[b] += 1
                else:
                    out[a] += 0.5
                    out[b] += 0.5
    for a in range(POPULATION):
        for b in range(len(toBeat)):
            if b != 2: continue #only paper
            winner = test(current[a],toBeat[b])
            if winner == 'A':
                out[a] += (2*POPULATION-1)
                names = ['rock','imp','paper']
                print(f'WINNER AGAINST {names[b]}:',current[a].toStr())
    return out
def outToPercentages(outs):
    percs = []
    total = sum(outs)
    for i in outs:
        percs.append(i/total)
    return percs
def getIndex(num,percentages):
    value = 0
    for i,p in enumerate(percentages):
        value += p
        if value > num:
            return i
    raise ValueError('This shouldn"t happen')
def findTops(outs):
    tops = []
    s = list(reversed(sorted(outs)))
    for n in range(NUM_CLONES):
        for i in range(len(outs)):
            if outs[i] == s[n] and i not in tops:
                tops.append(i)
                break
    return tops

if __name__ == '__main__':
    currentPets = []
    for i in range(POPULATION):
        currentPets.append(Brain())

    currentRound = 0

    imp = Brain()
    imp.instructions = [['MOV','$0','$1']]
    rock = Brain()
    rock.instructions = [['ADD','#50','$3'],['MOV','$2','@2'],['JMP','$-2','$0']]
    paper = Brain()
    paper.instructions = [['ADD', '#12', '$-1'], ['MOV', '@-2', '<5'], ['DJN', '$-1', '$-3'], ['SPL', '@3', '$0'], ['ADD', '#635', '$2'], ['JMZ', '$-5', '$-6'], ['DAT', '#0', '#833']]

    
    while True:
        print(currentRound)
        currentRound += 1
        
        outs = playRound(currentPets,[rock,imp,paper])
        percentages = outToPercentages(outs)

        print(max(outs))
        print()

        maxIndex = outs.index(max(outs))

        nextGen = [currentPets[i] for i in findTops(outs)]
        for i in range(NUM_RANDOM):
            nextGen.append(Brain())
        for i in range(POPULATION-NUM_CLONES-NUM_RANDOM):
            father = currentPets[getIndex(random.random(),percentages)]
            
            nextGen.append(Brain(parent=father))

        currentPets = nextGen
