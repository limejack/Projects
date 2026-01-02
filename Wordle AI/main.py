import math
def comp(word,win):
    out = []
    for i in range(5):
        if word[i] == win[i]:
            out.append((word[i],'correct',i))
        elif word[i] in win:
            out.append((word[i],'missed',i))
        else:
            out.append((word[i],'wrong',i))
    return out
def fromIn(word,line):
    out = []
    for i in range(5):
        if line[i] == '1':
            out.append((word[i],'correct',i))
        elif line[i] == '2':
            out.append((word[i],'missed',i))
        else:
            out.append((word[i],'wrong',i))
    return out
            
def remove(c,poss,m):
    out = []
    for i in range(len(poss)):
        add = True
        if len(out) + len(poss)-i < m:
            return -math.inf
        for j in c:
            if j[1] == 'correct':
                if poss[i][j[2]] != j[0]:
                    add = False
            elif j[1] == 'missed' :                    
                if j[0] not in poss[i] or poss[i][j[2]] == j[0]:
                    add = False
            else:
                if j[0] in poss[i]:
                    add = False
        if add:
            out.append(poss[i])
    return out
def score(word,poss,c,minimum):
    out = []
    m = 0
    for win in poss:
        s = c+comp(word,win)
        lis = remove(s,poss,0)
        out.append((len(lis),lis))
        if out[-1][0] > m:
            m = out[-1][0]
        if m > minimum:
            return (math.inf,[])
    return max(out)
        
def main():
    with open('dictionary.txt') as file:
        dictionary = file.read().split('\n')
    out = []
    word = 'arise'
    c = []
    poss = dictionary
    for i in range(5):
        newLine = input('What did you get?')
        out = []
        c += fromIn(word,newLine)
        poss = remove(c,poss,-math.inf)
        print(poss)
        minimum = math.inf
        for w in dictionary:
            out.append(score(w,poss,c,minimum))
            if out[-1][0] < minimum:
                minimum = out[-1][0]
        word = dictionary[out.index(min(out))]
        print(min(out)[0],word)    

if __name__ == '__main__':
    main()
