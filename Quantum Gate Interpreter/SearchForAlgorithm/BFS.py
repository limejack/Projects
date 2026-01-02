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

def fun(mainState,n):
    if n == 0:
        pass
    if n == 1:
        CNOT(mainState,[0,1])
    if n == 2:
        NOT(mainState,[0])
        CNOT(mainState,[0,1])
        NOT(mainState,[0])
    if n == 3:
        NOT(mainState,[1])
        
def checkState(state,n):
    for i,amp in enumerate(state.probAmps):

        if n==0 and amp != 0 and state.states[i] != '00':
            return False
        elif n!=0 and amp != 0 and state.states[i] != '01':
            return False

        
    return True

def evaluate(circuit):
    states = [State(),State(),State(),State()]
    for i in range(len(states)):
        state = states[i]
        state.addQBit(1,0)
        state.addQBit(1,0)
        for g in circuit:
            if g == 'H0':
                H(state,[0])
            elif g == 'H1':
                H(state,[1])
            elif g == 'F':
                fun(state,i)
            elif g == 'N0':
                NOT(state,[0])
            elif g == 'N1':
                NOT(state,[1])
            elif g == 'CNOT0':
                CNOT(state,[0,1])
            elif g == 'CNOT1':
                CNOT(state,[1,0])
            elif g == 'Z0':
                Z(state,[0])
            elif g == 'Z1':
                Z(state,[1])

        if not checkState(state,i):
            return False
    return True

if __name__ == '__main__':
    frontier = [[]]
    
    while frontier:
        current = frontier.pop(0)
        if len(current) > 6:
            continue

        if evaluate(current):
            print('ANSWER:',current)
            break

        for i in ['H0','H1','F','N0','N1','CNOT0','CNOT1','Z0','Z1']:
            child = current[:] + [i]
            frontier.append(child)
    print('DONE')
    
