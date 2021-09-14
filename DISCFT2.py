from math import pi,sin,cos,exp
from COOGRID2 import COOGRID
import numpy as np
from tkinter import messagebox
from function import *
import mpmath
import time
import scipy.special

def DISCFT(FX,FY,DEXT,DINT,FT=None,XFT=None,YFT=None,SINGLE=None):

    start = time.time()

    # some intermediate variables
    rho = (FX**2 + FY**2)**0.5



    if (not (XFT != None)) and (not (YFT != None)) and (not (FT != None)):
        FT=int(1) #应为byte型
        basic='y'
    if FT != None :
        ft=np.full(shape=(int(FX.shape[0]),int(FX.shape[1])),fill_value=0.0)
    if XFT != None :
        ftx=np.full(shape=(int(FX.shape[0]),int(FX.shape[1])),fill_value=0.0)
    if YFT != None :
        fty=np.full(shape=(int(FX.shape[0]),int(FX.shape[1])),fill_value=0.0)

    w1 = (rho == 0)
    w2 = (rho > 0)

    if not w1.any() == False:
        if FT != None:
            ft[w1]=pi*((0.5*DEXT)**2-(0.5*DINT)**2)
        if XFT != None:
            ftx[w1] = 0
        if YFT != None:
            fty[w1] = 0

    if not w2.any() == False :
        if FT != None:
            ft[w2] = (0.5 * DEXT) *scipy.special.jv(1,2 *pi * (0.5 * DEXT) * rho[w2]) / rho[w2] - (0.5 * DINT) * scipy.special.jv(1,2 *pi * (0.5 * DINT) * rho[w2]) / rho[w2]

        if XFT != None:
            ftx[w2] = ((0.5 * DEXT) * float(FX[w2]) / rho[w2] ** 3 * (pi * (0.5 * DEXT) * rho[w2] * (scipy.special.jv(0,2 *
                      pi * (0.5 * DEXT) * rho[w2]) - scipy.special.jv(2 *pi * (0.5 * DEXT) * rho[w2], 2))-scipy.special.jv(1,2 *pi * (0.5 * DEXT) * rho[w2]))
                      -(0.5 * DINT) * float(FX[w2]) / rho[w2] ** 3 * (pi * (0.5 * DINT) * rho[w2] * (scipy.special.jv(0,2 *pi * (0.5 * DINT) * rho[w2])
                      -scipy.special.jv(2,2 *pi * (0.5 * DINT) * rho[w2]))-scipy.special.jv(1,2 *pi * (0.5 * DINT) * rho[w2]))) / ( 2 *pi)
        if YFT != None :
            ftx[w2] = ((0.5 * DEXT) * float(FX[w2]) / rho[w2] ** 3 * (pi * (0.5 * DEXT) * rho[w2] * (scipy.special.jv(0,2 *
                       pi * (0.5 * DEXT) * rho[w2]) - scipy.special.jv(2,2 * pi * (0.5 * DEXT) * rho[w2])) - scipy.special.jv(1,2 * pi * (0.5 * DEXT) * rho[w2]))
                        - (0.5 * DINT) * float(FX[w2]) / rho[w2] ** 3 * (pi * (0.5 * DINT) * rho[w2] * (scipy.special.jv(0,2 * pi * (0.5 * DINT) * rho[w2])
                        - scipy.special.jv(2,2 * pi * (0.5 * DINT) * rho[w2])) - scipy.special.jv(1,2 * pi * (0.5 * DINT) * rho[w2]))) / (2 * pi)

    end = time.time()
    # print('DISCFT用时' +str(end-start))

    if not (SINGLE != None) :
        if n_elements(basic) != 0 :
            return (ft)





