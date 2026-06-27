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
        while l1 and l2 :
            if l1.val + l2.val   >=  10 :
                if counter :
                    add= str(l1.val + l2.val +1)
                    tail.next=ListNode(int(add[1]))
                    counter=True
                else :
                    add= str(l1.val + l2.val)
                    tail.next = ListNode(int(add[1]))
                    counter=True
               
            else:
                if counter :
                    if l1.val + l2.val +1 >=  10:
                        add= str(l1.val + l2.val +1)
                        tail.next = ListNode(int(add[1]))
                        counter=True
                    else:
                        tail.next = ListNode(l1.val+l2.val +1)
                        print(tail.next.val)
                        counter = False

                else:    
                    tail.next=ListNode(l1.val+l2.val )
            tail= tail.next
            l1=l1.next
            l2= l2.next
        while l1 :
            
            if counter : 
                if l1.val  +1 >=  10:
                    add= str(l1.val +1 )                     
                    tail.next = ListNode(int(add[1]))
                    counter=True
                    l1=l1.next
                    tail = tail.next
                else:
                    tail.next = ListNode(l1.val +1)
                    
                    counter=False
                    tail= tail.next
                    l1=l1.next
            else:
                tail.next = l1
                break
        while l2  :
            if counter : 
                if l2.val  +1 >=  10:
                    add= str(l2.val +1)
                    tail.next = ListNode(int(add[1]))
                    counter=True
                    tail= tail.next
                    l2=l2.next
                else:
                    tail.next = ListNode(l2.val +1)
                    counter=False
                    tail= tail.next
                    l2=l2.next
                
            else:
                tail.next = l2
                break
        if counter :
            tail.next= ListNode(1)



            

            
        
        


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