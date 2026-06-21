from typing import List
import numpy  as np 
a = np.array([
    [ 0.021, 0.018, 0.030, 0.025],
    [-0.015,-0.012,-0.020,-0.017],
    [ 0.032, 0.028, 0.041, 0.035],
    [ 0.018, 0.015, 0.022, 0.019],
    [-0.023,-0.019,-0.030,-0.025],
    [ 0.027, 0.024, 0.035, 0.029],
    [ 0.015, 0.013, 0.018, 0.016],
    [-0.018,-0.015,-0.024,-0.020]
])
def PCA(a:np.ndarray):
    mean = np.mean(a, axis=0)
    
    centerd_data=(a-mean)
    print('\n'"****** THE VARIANCE OF CENTERED DATA *********", np.var(centerd_data,axis=0),'\n')
    atransposed = np.transpose(centerd_data)
    covar= (np.matmul(atransposed,centerd_data))/(len(a)-1)
    print('\n'"******  COVAR ********* \n", covar,'\n')

    values , veceetors = np.linalg.eigh(covar)
    print('\n ',np.flip(veceetors, axis=1), '\n')
    veceetors=np.flip(veceetors, axis=1)
    PCA = np.matmul(centerd_data,veceetors)
    print('\n'"****** THE VARIANCE OF PCA DATA *********", np.var(PCA,axis=1),'\n')
    print('\n'"******  eignvalues  *********", values,'\n')

    return PCA

    

b = PCA(a)
print(b)