from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import deque
from collections import OrderedDict
control = np.random.normal(50,8,40)
treatment =np.random.normal(54,8,40)
alpha= 0.05

ttest= stats.ttest_ind(control,treatment)

print(ttest)