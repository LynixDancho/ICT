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
        counter=0
        while l1 and l2 or counter :
         value1= l1.val if l1 else 0 
         value2 = l2.val if l2 else 0
         add  = value1 + value2 + counter
         counter = add // 10 
         add = add% 10
         tail.next = ListNode(add)
         tail= tail.next
         l1=l1.next if l1 else l1 
         l2=l2.next if l2 else l2

         


        return head.next



# l1 = [9,9,9,9]
l1 = ListNode(9)
l1.next = ListNode(9)
l1.next.next = ListNode(9)
l1.next.next.next = ListNode(9)

# l2 = [9,9,9,9,9,9,9]
l2 = ListNode(9)
l2.next = ListNode(9)
l2.next.next = ListNode(9)
l2.next.next.next = ListNode(9)
l2.next.next.next.next = ListNode(9)
l2.next.next.next.next.next = ListNode(9)
l2.next.next.next.next.next.next = ListNode(9)

 
v= Solution.addTwoNumbers(None,l1,l2)

while v:
    print(v.val,'--->')
    v=v.next