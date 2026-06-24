from typing import List
import numpy  as np 
import matplotlib.pyplot as pl
import scipy.optimize as sc
def objective(x):
    x1=x[0]
    y=x[1]


    obj = x1**2 + y**2
    return obj 


def constraint1(x):
    y=x[1]
    x1=x[0]
    return x1+y-1 




x0= [1,1]
 
print(objective(x0))

cons ={
    'type': 'eq' , 'fun':constraint1
}

s= sc.minimize(objective,x0,method='SLSQP',constraints=cons) 
print(s)
