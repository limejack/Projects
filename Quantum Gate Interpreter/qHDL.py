from quantumSim import *
import re,math

primalGates = ['H','TOFF','MEASURE','X','Y','Z','CNOT','Grover','Flip']

def generateInputDict(inputs):
    out = {}
    for i in enumerate(inputs):
        out[i[1]] = i[0]
    return out

def evaluateGate(mainState,gateName,inputs):
    if gateName in primalGates:
        eval(gateName+'(mainState,['+','.join(map(str,inputs))+'])')
        return
    rawInput = open('Gates/'+gateName+'.gate').read()
    inputing = True
    inputPins = []
    procedure = []
    for line in rawInput.splitlines():
        if line == 'INPUTS:':
            continue
        elif line == 'PROCEDURE:':
            inputing = False
        elif inputing:
            for i in line.split(','):
                inputPins.append(i)
        else:
            procedure.append(line)

    inputDict = generateInputDict(inputPins)

    for i in procedure:
        gateName,pins = i[:-1].split('(')
        pinNumber = [inputs[inputDict[j]] for j in pins.split(',')]
        evaluateGate(mainState,gateName,pinNumber)

if __name__ == '__main__':
    fileToOpen = 'MUX.gate'

    ONE = (complex(0),complex(1))
    ZERO = (complex(1),complex(0))

    mainState = State()
    mainState.addQBit(*ONE)
    evaluateGate(mainState,fileToOpen,[0])

