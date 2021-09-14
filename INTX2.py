from function import *

def intx(DIM,XMIN,XMAX):

    # VALID_INPUT('INTX.PRO', 'N', DIM, 'integer', 0, 'no', '++', 1)
    # VALID_INPUT('INTX.PRO', 'DX OR XMIN', XMIN, 'real', 0, 'no', 'free', 'free')
    # VALID_INPUT('INTX.PRO', 'XMAX', XMAX, 'real', 0, 'no', 'free', 'free')

    minX = float(XMIN)
    maxX = float(XMAX)

    a=float(maxX) - float(minX)
    b=DIM - 1
    c=a/b
    d=dindgen(DIM)
    e=c*d
    f=e+minX

    return reform((float(maxX)-float(minX))/(DIM-1)*dindgen(DIM)+float(minX),[])

# print(intx(19,0.05,0.95))

# 结果：[0.05 0.1  0.15 0.2  0.25 0.3  0.35 0.4  0.45 0.5  0.55 0.6  0.65 0.7
#  0.75 0.8  0.85 0.9  0.95]