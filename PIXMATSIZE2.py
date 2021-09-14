from math import pi,sin,cos,exp
import numpy as np
from tkinter import messagebox
from function import *
from ATTOS_FWHM2 import ATTOS_FWHM
import time
#import numba as nb

#@nb.jit()
def PIXMATSIZE(MIRROR, DXF, N_PSF, LAM, W0, L0, ZA, HEIGHT, DISTCN2,P10, P11, P12, P13, P14, P15, P16, P17, INFO):

    start = time.time()

    WIND = P10
    WFSPITCH = P11
    DM_HEIGHT = P12
    SO_ANG = P13
    SO_ORI = P14
    WFS_INT = P15
    LAG = P16
    glao_wfs = P17

    # OTHER SETTINGS
    rad2asec = 3600.0* 180.0/pi
    asec2rad = 1.0/rad2asec

    #NYQUIST AND USER REQUESTED PSF PIXEL SIZE -> dxf_nyq, dxf_usr [asec/px]
    dxf_nyq = 1.0e-6*LAM/2.0/float(MIRROR['DEXTMAX'])*rad2asec  # Nyquist pixel size [asec/px]
    dxf_usr = dxf_nyq/(-DXF)

    # PSF FIELD-OF-VIEW -> fov_psf [asec]
    fov_fwhm = 8   # the FoV must be 8 times the PSF fwhm
    fov_psf = fov_fwhm*1.0e-6*LAM/float(MIRROR['DEXTMAX'])*rad2asec
    W0rad = float(W0)*asec2rad
    r0500 = 0.98*0.5e-6/W0rad*cos(float(ZA)/180*pi)**(3.0/5)
    r0LAM = r0500*(LAM/0.5)**(1.2)

    aos = (ATTOS_FWHM(float(MIRROR['DEXTMAX'])/r0LAM,float(MIRROR['DEXTMAX'])/L0))
    #aos=0.7255793948599701


    fov_psf = fov_fwhm * 1.0e-6*LAM/float(MIRROR['DEXTMAX']) * ((aos * 0.98 * float(MIRROR['DEXTMAX']) / r0LAM) ** 2 + 1) ** 0.5 * rad2asec
    pitch = r0LAM

    fov_psf = max([fov_psf, 4 * LAM * 1.0e-6/ pitch * rad2asec])

    # LAYERS MEAN ALTITUDE
    ndcn2 = DISTCN2 /total(DISTCN2)


    meanalti = total(ndcn2 * abs(HEIGHT/cos(float(ZA) / 180 *pi)) ** (5.0/3)) ** (3.0/5)

    meanwind = total(ndcn2*(((WIND[0,:]**2 + (WIND[1,:] * cos(float(ZA)/180*pi))**2)**0.5)**(5.0/3)))**(3.0/5)


    alpha = SO_ANG * np.array([cos(float(SO_ORI) / 180.0 * pi), sin(float(SO_ORI) / 180.0 * pi)])

    dtheta = (((glao_wfs['ang'][:, 0] - alpha[0]) ** 2 + (glao_wfs['ang'][:, 1] - alpha[1]) ** 2) ** 0.5)

    for igs in range(n_elements(glao_wfs['ang'][:, 0]) - 1):
        for jgs in range(igs, n_elements(glao_wfs['ang'][:, 0]) - 1):
            dtheta = np.append(dtheta, ((glao_wfs['ang'][igs, 0] - glao_wfs['ang'][jgs, 0]) ** 2 + (
                        glao_wfs['ang'][igs, 1] - glao_wfs['ang'][jgs, 1]) ** 2) ** 0.5)

    dtheta = max(dtheta)

    dfp_lf = 1.0/(100*pitch)

    dfp_lf = min([dfp_lf, 1.0/2/MIRROR['DEXTMAX']])

    if dtheta*meanalti > 0 :
        dfp_lf=min([dfp_lf,0.2/(meanalti*dtheta*asec2rad)])

    if typeof(size) != None :
        if (WFS_INT+2*LAG)*meanwind > 0 :
            dfp_lf=min([dfp_lf,0.2/((WFS_INT+2*LAG)*1-3*meanwind)])

    n_lf = 2 * (1.0 / 2 / pitch / dfp_lf) + 1

    if n_lf - int(n_lf) <= 0.01 :
        n_lf=int(n_lf)   #应转为 long 型
    if n_lf - int(n_lf) > 0.01 :
        n_lf = int(n_lf) + 1  #应转为 long 型
    if n_lf % 2 == 0 :
        n_lf=n_lf+1


    dfp_lf = 1.0 / (n_lf - 1) / pitch

    # size of extended low spatial frequency matrix (zero padded)
    n_lf_padded = fov_psf * asec2rad / (1.0e-6 * LAM * dfp_lf)

    if n_lf_padded - int(n_lf_padded) <= 0.01 :
        n_lf_padded=int(n_lf_padded)   # #应转为 long 型
    if n_lf_padded - int(n_lf_padded) > 0.01 :
        n_lf_padded=int(n_lf_padded) + 1  #应转为 long 型
    if n_lf_padded % 2 == 1 :
        n_lf_padded=n_lf_padded+1


    dxp = 1.0 / n_lf_padded / dfp_lf
    dff = dxp / (1e-6 * LAM)
    n_otf = 2 * float(MIRROR['DEXTMAX'] / (dff * 1e-6 * LAM))

    if n_otf - int(n_otf) > 0.01 :
        n_otf=int(n_otf)+1
    if n_otf - int(n_otf) <= 0.01 :
        n_otf=int(n_otf)
    if n_otf % 2 == 1 :
        n_otf=n_otf+1
    dfp = 1.0 / n_otf / dxp


    dxf_int = 1.0 / n_otf / dff * rad2asec
    n_psf_usr = fov_psf / dxf_usr
    if n_psf_usr - int(n_psf_usr) >= 0.01 :
        n_psf_usr=int(n_psf_usr)+1
    if n_psf_usr - int(n_psf_usr) < 0.01 :
        n_psf_usr=int(n_psf_usr)
    if n_psf_usr % 2 == 1 :
        n_psf_usr=n_psf_usr+1
    #print(n_psf_usr)
    n_psf_usr = max([n_psf_usr, n_otf])
    dxf_usr = fov_psf / n_psf_usr


    end = time.time()
    # print('PIXMATSIZE用时'+str(end-start))

    # 结果
    res = {'FOV_PSF': fov_psf, 'N_PSF_USR': n_psf_usr, 'DXF_USR': dxf_usr, 'DXF_INT': dxf_int, 'DXF_NYQ': dxf_nyq, 'N_OTF': n_otf,
           'DFF': dff, 'DXP': dxp, 'DFP': dfp, 'LAMBDA': LAM,'W0':W0,'W0_LLZ':0.98*LAM*1e-6/r0LAM*rad2asec*aos,'L0':L0,
           'ZA':ZA,'r0500':r0500,'r0LAM':r0LAM,'N_LF':n_lf,'N_LF_PADDED':n_lf_padded,'DFP_LF':dfp_lf,'WFSPITCH':pitch}
    return (res)


