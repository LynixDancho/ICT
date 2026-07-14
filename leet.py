from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import defaultdict
def heapify(array, i):
    left = 2*i +1 
    right = 2*i+2
    if left <  len(array) and array[left]< array[i]:
        max = left
    else :
        max= i     
    if right <  len(array) and array[right] < array[max]:
        max = right
    if ( max !=i ):
        array[i],array[max] = array[max],array[i]
        heapify(array,max)

def build_max_heap(array):
    
    for i in range(len(array)//2,-1,-1):
        heapify(array,i)


def heapsort(array):
    build_max_heap(array)
    for i in range(len(array)-1,-1,-1):
        print(i)
        array[i],array[0]= array[0],array[i]
        heapify(array,i)
    print(array)


nums = [14,55,66,34,22,12,33,44]
heapsort(nums)


print(nums)
