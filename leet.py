from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import re

def isBadVersion(version: int) -> bool:
        return version >= 3 

def firstBadVersion( n: int) -> int:
        
        l,r=0,n
        res=0
        while l<=r :
            m = l+((r-l)//2)
            if isBadVersion(m):
                r= m-1
                res=m
                print(res)
                
            elif not isBadVersion(m):
                l = m +1
        return res


x = firstBadVersion(5)
lt = list(range(1,5+1))

print(x)