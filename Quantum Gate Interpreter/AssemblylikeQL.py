from quantumSim import State
from qHDL import evaluateGate

def amplify():
    fileToOpen = 'C:/Users/edmun/Documents/Pythongames/Quantum/Working Quantum Interpreter/AssemblyCode/basicGrovers.QLA'
    rawInput = open(fileToOpen).read()
    mainState = State()
    ONE = (complex(0),complex(1))
    ZERO = (complex(1),complex(0))
    labels = {}

    lines = rawInput.splitlines()
    counter = 0
    
    for line in enumerate(rawInput.splitlines()):
        if line[1][:5] == 'LABEL':
            labels[line[1][6:]] = line[0]    
    while True:
        line = lines[counter]
        counter += 1
        
        if line == '' or line[0] == '#':
            continue
        elif line[:5] == 'LABEL':
            continue
        elif line[:3] == 'END':
            break
        elif line[:4] == 'GOTO':
            counter = labels[line.split(' ')[1]]
        
        functionName,functionInput = line.split('(')
        if functionName == 'init':
            for i in range(int(functionInput[:-1])):
                mainState.addQBit(*ZERO)
        elif functionName == 'output':
            return mainState.states,mainState.probAmps
        else:
            inputList = functionInput.split(')')[0].split(',')
            evaluateGate(mainState,functionName,list(map(int,inputList)))


if __name__ == '__main__':
    fileToOpen = 'AssemblyCode/basicGrovers.QLA'
    rawInput = open(fileToOpen).read()
    mainState = State()
    ONE = (complex(0),complex(1))
    ZERO = (complex(1),complex(0))
    labels = {}

    lines = rawInput.splitlines()
    counter = 0
    
    for line in enumerate(rawInput.splitlines()):
        if line[1][:5] == 'LABEL':
            labels[line[1][6:]] = line[0]    
    while True:
        line = lines[counter]
        counter += 1
        
        if line == '' or line[0] == '#':
            continue
        elif line[:5] == 'LABEL':
            continue
        elif line[:3] == 'END':
            break
        elif line[:4] == 'GOTO':
            counter = labels[line.split(' ')[1]]
        
        functionName,functionInput = line.split('(')
        if functionName == 'init':
            for i in range(int(functionInput[:-1])):
                mainState.addQBit(*ZERO)
        elif functionName == 'output':
            print(mainState)
        else:
            inputList = functionInput.split(')')[0].split(',')
            evaluateGate(mainState,functionName,list(map(int,inputList)))
