import math,random
class State():
    def __init__(self):
        self.states   = []
        self.probAmps = []
    def addQBit(self,stateZero,stateOne):
        outStates = []
        outAmps   = []
        if len(self.states) == 0:
            self.states = ['1','0']
            self.probAmps = [stateOne,stateZero]
        else:
            for i in range(len(self.states)):
                outStates.append(self.states[i]+'0')
                outAmps.append(self.probAmps[i]*stateZero)
                outStates.append(self.states[i]+'1')
                outAmps.append(self.probAmps[i]*stateOne)
            self.states = outStates
            self.probAmps = outAmps
    def __str__(self):
        out = []
        for i in range(len(self.states)):
            if self.probAmps[i] != 0:
                out.append(self.states[i]+' '+str(self.probAmps[i]))
        return '\n'.join(out)
    def measure(self,a):
        probA = 0
        probB = 0

        for i in range(len(self.states)):
            if self.states[i][a] == '1':
                probA += self.probAmps[i]*self.probAmps[i].conjugate()
            else:
                probB += self.probAmps[i]*self.probAmps[i].conjugate()
        if random.random() < probA:
            finalState = '1'
            finalProb = math.sqrt(probA)
        else:
            finalState = '0'
            finalProb = math.sqrt(probB)

        for i in range(len(self.states)):
            if self.states[i][a] != finalState:
                self.probAmps[i] = 0
            else:
                self.probAmps[i] /= finalProb

def gate(state,function,inputs):
    out = {}
    for i in range(len(state.states)):
        newStates,probAmps = function(state.states[i],inputs)
        for nState in enumerate(newStates):
            if nState[1] not in out: out[nState[1]] = 0
            out[nState[1]] += probAmps[nState[0]]*state.probAmps[i]
    outA = []
    outB = []
    for i in out:
        outA.append(i)
        outB.append(out[i])
    state.states = outA
    state.probAmps = outB


#Basic Gates
def h(state,inputs):
    outProbs = [1/math.sqrt(2) if state[inputs[0]] == '0' else -1/math.sqrt(2),1/math.sqrt(2)]
    outStats = [state[:inputs[0]]+'1'+state[inputs[0]+1:],
                state[:inputs[0]]+'0'+state[inputs[0]+1:]]
    return outStats,outProbs
def cnot(state,inputs):
    a = state[inputs[0]]
    b = state[inputs[1]]

    if a == '0':
        return [state],[1]
    elif b == '1':
        return [state[:inputs[1]]+'0'+state[inputs[1]+1:]],[1]
    elif b == '0':
        return [state[:inputs[1]]+'1'+state[inputs[1]+1:]],[1]
        
def toffoli(state,inputs):
    if state[inputs[0]] != '1' or state[inputs[1]] != '1':
        return [state],[1]
    if state[inputs[2]] == '0':
        return [state[:inputs[2]]+'1'+state[inputs[2]+1:]],[1]
    return [state[:inputs[2]]+'0'+state[inputs[2]+1:]],[1]
def pauliX(state,inputs):
    if state[inputs[0]] == '1':
        change = '0'
    else:
        change = '1'
    return [state[:inputs[0]]+change+state[inputs[0]+1:]],[1]
def pauliY(state,inputs):
    if state[inputs[0]] == '1':
        change = '0'
        prob = -1
    else:
        change = '1'
        prob = 1
    return [state[:inputs[0]]+change+state[inputs[0]+1:]],[complex(0,prob)]
def pauliZ(state,inputs):
    if state[inputs[0]] == '1':
        change = '1'
        prob = -1
    else:
        change = '0'
        prob = 1
    return [state[:inputs[0]]+change+state[inputs[0]+1:]],[complex(prob,0)]

def isSolution(solution):
    x = open('tempCNF.cnf').read()
    x = x.splitlines()
    out = []
    for i in x[1:]:
        line = list(map(int,i.split(' ')))[:-1]
        if not testLine(line,solution): return False
    return True
def testLine(line,solution):

    for i in line:
        if i > 0 and solution[abs(i)-1] == '1': return True
        elif i < 0 and not solution[abs(i)-1] == '0': return True
    return False

def grover(state,inputs):
    return [state],[-1 if isSolution(state) else 1]
def flip(state,inputs):
    if '1' not in state:
        return [state],[-1]
    return [state],[1]

def Flip(mainState,inputs):
    for i in inputs: gate(mainState,h,[i])
    gate(mainState,flip,inputs)
    for i in inputs: gate(mainState,h,[i])

def Grover(mainState,inputs):
    gate(mainState,grover,inputs)
def H(mainState,inputs):
    gate(mainState,h,inputs)
def TOFF(mainState,inputs):
    gate(mainState,toffoli,inputs)
def Z(mainState,inputs):
    gate(mainState,pauliZ,inputs)
def Y(mainState,inputs):
    gate(mainState,pauliX,inputs)
def X(mainState,inputs):
    gate(mainState,pauliX,inputs)
def CNOT(mainState,inputs):
    gate(mainState,cnot,inputs)
#Constructed Gates
def AND(mainState,inputs):
    gate(mainState,toffoli,inputs)
def NOT(mainState,inputs):
    gate(mainState,pauliX,inputs)
def OR(mainState,inputs):
    NOT(mainState,[0])
    NOT(mainState,[1])
    AND(mainState,inputs)
    NOT(mainState,[0])
    NOT(mainState,[1])
    NOT(mainState,[2])

if __name__ == '__main__':

    ONE = (complex(0),complex(1))
    ZERO = (complex(1),complex(0))
    stateToText = {ONE:'1',ZERO:'0'}

    inputs = [[ONE,ONE],[ONE,ZERO],[ZERO,ONE],[ZERO,ZERO]]
    for i in inputs:
        mainState = State()
        mainState.addQBit(*i[0])  #0:Input A
        mainState.addQBit(*i[1])  #1:Input B
        mainState.addQBit(*ZERO) #2:Destination Bit

        
        AND(mainState,[0,1,2])
        
        print(mainState)


    
