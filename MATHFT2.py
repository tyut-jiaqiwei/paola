from tkinter import messagebox
import numpy as np
from scipy import fft,ifft
from function import *
from DISCFT2 import DISCFT
from COOGRID2 import COOGRID
from math import pi,sin,cos,exp

def MATHFT(OBJECT ,DX=None,IC=None,JC=None,INVERSE=None,COO=None,SINGLE=None):

    sz = size(OBJECT)

    type = sizetype(OBJECT)

    #setting
    if DX == None :
        DX=1.0
    if IC == None :
        IC=0.0
    if JC == None :
        JC=0.0
    fNyqu = 0.5/float(DX)
    df = 1.0 / (OBJECT.shape[0] - (OBJECT.shape[0] % 2)) / float(DX)

    if sz[0] == 2:
        if SINGLE != None :
            tmp = (COOGRID(sz[1] - (sz[1] % 2), sz[1] - (sz[1] % 2), SCALE=fNyqu,SINGLE=1,FT=1,COO_X=1))['x']
            xc = IC * DX
            yc = JC * DX
            tmp = 2 * pi * (xc * tmp + yc * np.rot90(tmp, 3))
            tmp = dcomplex(cos(tmp), sin(tmp))
        else:
            tmp = (COOGRID(sz[1] - (sz[1] % 2), sz[1] - (sz[1] % 2), SCALE=fNyqu, FT=1, COO_X=1))['x']
            xc = IC * DX
            yc = JC * DX
            tmp = 2 * pi * (xc * tmp + yc * np.rot90(tmp, 3))
            tmp = dcomplex(np.cos(tmp), np.sin(tmp))


    if INVERSE == None :
        if sz[0] == 1 :
            tmp=tmp * shift(np.fft.fft(((OBJECT)[0,:])/size(OBJECT)[1], (sz[1] - (sz[1] % 2)) /2))/df
        if sz[0] == 2 :
            tmp=tmp * shift(np.fft.fft2(OBJECT/(size(OBJECT)[4])), (sz[1] - (sz[1] % 2)) / 2, (sz[1] - (sz[1] % 2)) / 2)/df**2

    else :
        if sz[0] == 1 :
            tmp=np.fft.ifft2(df * shift((OBJECT)[0:]/tmp, (sz[1] - (sz[1] % 2))/2)*size(OBJECT)[1])   # / inverse
        if sz[0] == 2 :
            tmp=np.fft.ifft2(df ** 2 * shift((OBJECT)/tmp, (sz[1] - (sz[1] % 2)) / 2, (sz[1] - (sz[1] % 2))/2)*(size(OBJECT)[4])) # / inverse


    if COO == None :
        return tmp
    return {'y': tmp, 'coo': abscissa}




