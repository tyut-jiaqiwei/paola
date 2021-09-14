
import numpy as np

from math import pi,sin,cos,exp
def SINC(X):

    if type(X) is np.ndarray:
        mat = X.copy()

        w = (X == 0)
        mat[w] = 1

        w = (X != 0)
        mat[w] = np.sin(pi * X[w])/ (pi * X[w])
        return mat
    else:
        num = X
        if X == 0 :
            num =1
        else :
            num = np.sin(pi * X) / (pi * X)
        return num

# 效果等同于np.sinc
# a=np.arange(100)/100
# print(SINC(a))
# print(np.sinc(a))
