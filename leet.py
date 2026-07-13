from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import defaultdict
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        compar=[]
        target=0

        nums.sort()
        for target , value in enumerate(nums):
            print(nums)

            if value > 0 :
                break
            if target> 0 and nums[target] == nums[target-1]:
                continue
            i=target+1
            j = len(nums)-1 
            while i < j :
                if nums[i]+nums[j ]+value ==0:
                    print(i , j, target)
                    compar.append([nums[i],nums[j ],value ])
                    j-=1
                    while nums[j] == nums[j+1] and j< len(nums)-2 and i<j:
                        j-=1
                elif nums[i]+nums[j ]+value>0:
                    j-=1
                else:
                    i+=1
        return compar
                

            


        

nums1 =[1,2,0,1,0,0,0,0]


x = Solution.threeSum(None,nums1)

print(x)
