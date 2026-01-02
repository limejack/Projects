from datetime import date
import matplotlib.pyplot as plt
import numpy as np

def read(filename):
    with open(filename) as infile:
        out = eval(infile.read())
    return out
def get_derv(x,y):
    first_derv = []#Size of 1 less than the dataset
    out_b = []
    for i in range(len(y)-1):
        first_derv.append((y[i+1]-y[i])/(x[i+1]-x[i]))
        out_b.append((x[i+1]-x[i])/2+x[i])
    return first_derv,out_b


data = read("C:/Users/tew31/OneDrive/Documents/GitHub/Projects/Finance Model Random Walk/Data/IBM.json")['Time Series (Daily)']

keys = list(data.keys())

x = []
y = []
for day in keys:
    x.append(date.fromisoformat(day).toordinal())
    y.append(float(data[day]['4. close']))

lin_slope = (y[-1]-y[0])/(x[-1]-x[0])
lin_inter = y[0]-lin_slope*x[0]
shifted = []
for a,b in zip(x,y):
    shifted.append(b-a*lin_slope-lin_inter)

first_derv_y,first_derv_x = get_derv(x,y)#Size of 1 less than the dataset

counts,boxes = np.histogram(first_derv_y,bins=100)

plt.stairs(counts,boxes)

plt.show()
