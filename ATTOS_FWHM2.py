import numpy as np
import math
from function import *
from INTX2 import intx
import time
#import numba as nb

#@nb.jit()
def ATTOS_FWHM(DSRO,DSLO):

    start = time.time()

    x = DSRO
    y = DSLO

    eta = np.zeros(shape=(1))

    #setting
    seuil = intx(19, 0.05, 0.95)
    p0 = np.array([-0.72745573, 10.709212, -70.269387, 309.73613, -787.28352, 1139.7155, -867.43459, 270.49072])
    p_al = np.array([1.4865041, -6.8220483, 26.357913, -58.126416, 49.818448])
    p_ah = np.array([1.0385946, -1.2779076, 0.55563972])
    p_bl = np.array([-0.85032682, 0.1097915, -1.8906293, 5.8972417, -7.1103492])
    p_bh = -0.99459798
    p_bg = np.array([-0.007354186, -0.13413489, 0.50041961, -0.7211639, 0.35597915])
    p_a1 = np.array([-0.1053306, 0.49817898, -8.1362721, 36.078945, -67.871138, 57.762569, -18.305613])
    p_b1 = np.array([0.18337032, 0.65239064, -3.1594634, 4.4308597, -2.0469633])
    p_c1 = np.array([1.56871, -9.1191115, 35.028754, -79.157739, 98.848737, -63.234645, 16.190233])
    p_a2 = np.array([-0.37286461, 2.2054525, -6.1531596, 7.6576049, -3.4316943])
    p_b2 = np.array([0.82357295, -6.8653591, 71.105413, -399.44691, 1152.6087, -1748.1104, 1327.9698, -398.23276])
    p_c2 = np.array([1.4882965, -12.286948, 121.74294, -740.05595, 2612.4161, -5428.8625, 6519.628, -4167.8742, 1094.2977])

    # CALCULATION
    for i_s in range(19):
        y0 = 10 ** poly(seuil[i_s], p0)
        a = (seuil[i_s] <= 0.5) * 10 ** poly(seuil[i_s], p_al) + (seuil[i_s] > 0.5) * 10 ** poly(seuil[i_s], p_ah)
        b = (seuil[i_s] <= 0.5) * poly(seuil[i_s], p_bl) + (seuil[i_s] > 0.5) * p_bh
        bg = poly(seuil[i_s], p_bg)
        a1 = poly(seuil[i_s], p_a1)
        b1 = poly(seuil[i_s], p_b1)
        c1 = poly(seuil[i_s], p_c1)
        a2 = poly(seuil[i_s], p_a2)
        b2 = poly(seuil[i_s], p_b2)
        c2 = poly(seuil[i_s], p_c2)
        tmp = y0 * a / (a + DSRO ** (-b)) * (1 + bg - a1 / (b1 + (math.log(DSRO,10) - c1) ** 2) - a2 / (b2 + (math.log(DSRO,10) - c2) ** 4))

        #print(tmp)
        if i_s == 0 :
            w = (tmp*DSLO >= 1)
            if not w.all() == False  :
                eta[w] = 0.05
            pre = tmp

        if i_s > 0 :
            w = (tmp*DSLO >= 1) & (pre*DSLO < 1)
            if not w.all() == False :
                slope = 0.05/(math.log(tmp,10)-math.log(pre,10))
                eta = slope * (math.log(1.0/DSLO,10)-math.log(pre,10))+seuil[i_s - 1]
            pre = tmp

        if i_s == 18:
            w = (tmp * DSLO < 1)
            if not w.all() == False :
                eta[w] = 1.0

    end = time.time()

    return eta
