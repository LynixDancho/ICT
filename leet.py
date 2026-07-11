from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
def Partition( array , left:int , right:int  ):
        i = left
        j= right-1
        pivot= array[right]
        while i<j:
                print(j )
                while array[i]<pivot and i<right:
                        i+=1
                while array[j]>= pivot and j>left:
                        j-=1
                        
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


start= time.perf_counter()

x = [1,2,2,2,2,2,2,2,2,5]
quicksort(x,0,len(x)-1)
end = time.perf_counter()
print(f"Time: {end - start:.6f} seconds")