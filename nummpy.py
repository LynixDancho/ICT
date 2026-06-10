import numpy as np

arr_2d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
arr_2d[:,1]=   np.flip(arr_2d[:,1])
print(arr_2d)
 