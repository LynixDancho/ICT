from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import OrderedDict
class LRUCache:
    def __init__(self,capacity):
        self.capacity= capacity
        self.cache = OrderedDict()
    def get(self,key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
    def put(self,key,value):
        if key  in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache)> self.capacity:
            self.cache.popitem(last=False)
        
        
        


print(nums)
