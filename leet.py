from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as plt
from scipy import stats
import time
from collections import deque
from collections import OrderedDict


        
class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
class Solution:
    def sortList(self, head: ListNode) -> ListNode:
        tail = head
        hail = head 
        i=0
        max= [] 
        while tail :
             max.append(tail.val)
             tail = tail.next  
        max.sort()
        while i < len(max):
            head.val = max[i]
            head = head.next
            i+=1
        
        return hail 


head = [4,2,1,3] 
