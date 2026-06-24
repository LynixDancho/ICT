from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as pl
import scipy.optimize as sc
def taylor_sin(x):
    res = x-(x**3)/m.factorial(3)+(x**5)/m.factorial(5)-(x**7)/m.factorial(7)+(x**9)/m.factorial(9)
    return res


#for i in np.linspace(-3, 3, 100):
    v =np.sin(i)
    y=  taylor_sin(i)
    x=v-y
    pl.plot(i,x,'b.')
     

pl.show()
print(f'the taylor sin is {taylor_sin(-1.5)} and tru value of sin is {np.sin(-1.5)}')