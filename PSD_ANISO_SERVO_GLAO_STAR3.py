from COOGRID2 import COOGRID
from function import *
import numpy as np
from SINC2 import SINC
# import numba as nb
from math import pi,sin,cos,exp
import time
from numba import njit, config, __version__
from numba import prange



# @nb.jit(nopython=True)
def PSD_ANISO_SERVO_GLAO_STAR(N_PSD,FPCOO,LAM,HEIGHT,WIND,r0500_i,L0,WFSPITCH,DMTF,DM_HEIGHT,SO_ANG,SO_ORI,WFS_INT,LAG,GS_WEIGHT,GLAO_WFS,PRECISION):
    ang = GLAO_WFS['ang']
    start = time.time()

    # settings
    asec2rad = 1.0/ 3600.0/ 180.0*pi
    alpha = SO_ANG * np.array([np.cos(float(SO_ORI) / 180.0 * pi), np.sin(float(SO_ORI) / 180.0 * pi)]) * asec2rad

    fc_pupil = 0.5/WFSPITCH*(1 + 1e-3)

    w = (FPCOO ** 2 + rotate(FPCOO, 3)**2>0) & (abs(FPCOO)<fc_pupil) & (abs(rotate(FPCOO, 3))<fc_pupil)
    psd=np.zeros(shape=(int(N_PSD), int(N_PSD)))
    nstars = len(GLAO_WFS['ang'][:,0])


    # GS weight setting
    if n_elements(GS_WEIGHT)  == 1 :
        gsw=np.zeros(shape=(int(nstars))) +1.0 / nstars
    if n_elements(GS_WEIGHT)  != 1 :
        gsw=GS_WEIGHT
    gsw = gsw /total(gsw)

    # PSD computation
    if strlowcase(PRECISION) == 'single' :
        pass
    else:
        for indlayer in range(len(HEIGHT)):
            filtre = np.zeros(shape=(int(N_PSD), int(N_PSD)))
            dtfvl = 1e-3 * WFS_INT * (FPCOO * WIND[0][indlayer] + rotate(FPCOO, 3) * WIND[1][indlayer])
        #     for indstar in range(nstars):
        #
        #         argcos = FPCOO * (1e-3 * LAG * WIND[0][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstar][0] * asec2rad - alpha[0])) +\
        #                 rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstar][1] * asec2rad - alpha[1]))
        #
        #         filtre = filtre + gsw[indstar] ** 2 * (1 - 2 * DMTF * SINC(dtfvl) * np.cos(2 *pi * argcos) + DMTF ** 2 * SINC(dtfvl) ** 2)
        #
        #
        #     for indstari in range(nstars-1) :
        #         for indstarj in range(indstari+1,nstars):
        #             # argcosi, argcosj, argcosji, filtre = formula(FPCOO, LAG, WIND, HEIGHT, indlayer, DM_HEIGHT, GLAO_WFS['ang'], indstari, asec2rad, alpha, filtre, indstarj, gsw, DMTF, dtfvl)
        #             argcosi = FPCOO * (1e-3 * LAG * WIND[0][indlayer]+ abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstari][0] * asec2rad - alpha[0])) +\
        #             rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstari][1] * asec2rad - alpha[1]))
        #
        #             argcosj = FPCOO * (1e-3 * LAG * WIND[0,indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstarj,0] * asec2rad - alpha[0])) +\
        #             rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstarj][1] * asec2rad - alpha[1]))
        #
        #             argcosji = FPCOO * abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstarj][0] - GLAO_WFS['ang'][indstari][0]) * asec2rad +\
        #             rotate(FPCOO, 3) * abs(HEIGHT[indlayer] - DM_HEIGHT) * (GLAO_WFS['ang'][indstarj][1] - GLAO_WFS['ang'][indstari][1]) * asec2rad
        #
        #             filtre = filtre + 2 * gsw[indstari] * gsw[indstarj] * (1 - DMTF * SINC(dtfvl) * (np.cos(2 *pi * argcosi) + np.cos(2 *pi * argcosj))+\
        #             DMTF ** 2 * SINC(dtfvl) ** 2 * np.cos(2 *pi * argcosji))

            argcosi, argcosj, argcosji, filtre = formula(HEIGHT,N_PSD,WFS_INT,FPCOO,WIND,nstars,LAG,DM_HEIGHT,ang,asec2rad,alpha,gsw,DMTF,dtfvl,filtre,indlayer)
            psd[w] = psd[w] + (r0500_i[indlayer] * (LAM / 0.5) ** (6.0/ 5)) ** (-5.0/ 3) * filtre[w]
        psd[w] = 0.022896 * (FPCOO[w] ** 2 + (rotate(FPCOO, 3))[w] ** 2 + float (L0 != -1) / L0 ** 2) ** (-11.0 / 6.0) * psd[w]

    end = time.time()
    # print('PSD_ANISO_SERVO_GLAO_STAR用时'+str(end-start))

    return psd


# @nb.jit(nopython=True)
#@njit(parallel=True)
def formula(HEIGHT,N_PSD,WFS_INT,FPCOO,WIND,nstars,LAG,DM_HEIGHT,ang,asec2rad,alpha,gsw,DMTF,dtfvl,filtre,indlayer) :
    for indstar in range(nstars):
        argcos = FPCOO * (1e-3 * LAG * WIND[0][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (ang[indstar][0] * asec2rad - alpha[0])) + \
                 rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (ang[indstar][1] * asec2rad - alpha[1]))

        filtre = filtre + gsw[indstar] ** 2 * (1 - 2 * DMTF * np.sinc(dtfvl) * np.cos(2 * pi * argcos) + DMTF ** 2 * np.sinc(dtfvl) ** 2)

    for indstari in range(nstars - 1):
        for indstarj in range(indstari + 1, nstars):
            # argcosi, argcosj, argcosji, filtre = formula(FPCOO, LAG, WIND, HEIGHT, indlayer, DM_HEIGHT, GLAO_WFS['ang'], indstari, asec2rad, alpha, filtre, indstarj, gsw, DMTF, dtfvl)
            argcosi = FPCOO * (1e-3 * LAG * WIND[0][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                        ang[indstari][0] * asec2rad - alpha[0])) + \
                      rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                        ang[indstari][1] * asec2rad - alpha[1]))

            argcosj = FPCOO * (1e-3 * LAG * WIND[0, indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                        ang[indstarj, 0] * asec2rad - alpha[0])) + \
                      rotate(FPCOO, 3) * (1e-3 * LAG * WIND[1][indlayer] + abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                        ang[indstarj][1] * asec2rad - alpha[1]))

            argcosji = FPCOO * abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                        ang[indstarj][0] - ang[indstari][0]) * asec2rad + \
                       rotate(FPCOO, 3) * abs(HEIGHT[indlayer] - DM_HEIGHT) * (
                                   ang[indstarj][1] - ang[indstari][1]) * asec2rad

            filtre = filtre + 2 * gsw[indstari] * gsw[indstarj] * (
                        1 - DMTF * np.sinc(dtfvl) * (np.cos(2 * pi * argcosi) + np.cos(2 * pi * argcosj)) + \
                        DMTF ** 2 * np.sinc(dtfvl) ** 2 * np.cos(2 * pi * argcosji))
    return argcosi, argcosj, argcosji, filtre



# @nb.jit(nopython=True)
#@njit(parallel=True)
def rotate(array,num):
    for k in range(num):
        temp = np.zeros_like(array.transpose())
        for j in range(len(array)):
            for i in range(len(array[0])):
                temp[i][j] = array[j][len(array[0])-i-1]
        array = temp
    return array