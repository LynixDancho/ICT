from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
def montecarlo(numberofrols):
    x= np.random.randint(1,7,numberofrols)
    #y= np.random.randint(1,7,numberofrols)
     
    x = np.array(x)
    sum = np.sum(x)
    return sum/numberofrolls



numberofrolls = 10000

counts = montecarlo(numberofrolls)
counts = np.array(counts)

print(counts)

 
