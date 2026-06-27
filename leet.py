from typing import List
import numpy  as np 
import math as m
import matplotlib.pyplot as pl
import scipy.optimize as sc
class ListNode:
    def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        head = ListNode()
        tail = head
        counter=False
        while l1 and l2:
            if l1.val+l2.val >= 10 :
                z= str(l1.val+l2.val)
                tail.next =  ListNode(int(z[1]))
                
                
                
                counter=True
            else :
                z= l1.val+l2.val
                if counter:
                    z+=1
                    counter = False
                    tail.next=ListNode(z)
            tail = tail.next
            l1= l1.next
            l2 = l2.next
        if l1 and not l2 :
            tail.next = l1 
        else :
            tail.next = l2
        if counter  and not l1 | l2 :
            tail = tail.next
            tail.next = 1 
            Counter = False
        

        return head.next


# l1 = [2,4,3]
l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

# l2 = [5,6,4]
l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)
v= Solution.addTwoNumbers(None,l1,l2)

print(v)