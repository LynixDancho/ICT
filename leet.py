from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import deque
from collections import OrderedDict
import pandas as pd 


df = pd.read_csv("./housing.csv")


print(df)