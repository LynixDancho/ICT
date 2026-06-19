from typing import List
import numpy  as np 
a = [
    [2, 0, 0, 0],
    [0, 3, 0, 0],
    [0, 0, 4, 0],
    [0, 0, 0, 5]
]
def determinant(a:List[int]):
    det=0
    if len(a) == len(a[0]):
        if len(a) == 2:
            b= a[0][0]*a[1][1] - a[0][1]*a[1][0]
            return b 
        for c in range(len(a)):

            newMatrice=[
                [x for j , x in enumerate(row) if j!=c]for i, row in enumerate(a) if i!=0  
                ]
            det += (-1)**c  * a[0][c] * determinant(newMatrice)
            


        return det
b=np.array([[4,2],[1,3]])
eigval =np.linalg.svd(a)
print(eigval)