from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import re
def Partition( array , left:int , right:int  ):
        i = left
        j= right-1
        pivot= array[right]
        while i<j:
                while array[i]<pivot and i<right:
                        i+=1
                while array[j]> pivot and j>left:
                        j-=1
                        print(j)
                if i<j:
                        array[i], array[j]= array[j],array[i]

        if array[i] >pivot:
                array[i], array[right]= array[right], array[i]
        return i 
 
def quicksort(array, left:int , right:int ):
    if left<right:
        partition = Partition(array, left,right)
        quicksort(array ,left ,partition-1)
        quicksort(array, partition+1, right)



x = [1,4,5,3,2,6,8]
quicksort(x,0,len(x)-1)

print(x)