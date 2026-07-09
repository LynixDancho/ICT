from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import re
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        i = 0 
        j= 0 
        newmerged=[]
        mediane= 0 
        while i <= len(nums1)-1 or j <= len(nums2)-1:
            if i >= len(nums1) and j < len(nums2):
                
                newmerged.append(nums2[j])
                j+=1
                continue
            if i < len(nums1) and j >= len(nums2):
                newmerged.append(nums1[i])
                i+=1   
                continue             
            
            if nums1[i]< nums2[j]:
                newmerged.append(nums1[i])
                i+=1
            else:
                newmerged.append(nums2[j])
                j+=1
        if newmerged: 
            middle = len(newmerged) //2 
            mediane =( (newmerged[middle] + newmerged[middle-1])/2) if (len(newmerged) %2 ) == 0 else newmerged[middle]

        return mediane





test = []
gg=[]
x = Solution.findMedianSortedArrays(None,test,gg)

 
print(x)