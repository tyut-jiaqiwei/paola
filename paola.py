from math import pi,sin,cos,exp
import numpy as np
from tkinter import messagebox
from function import *
from PIXMATSIZE2 import PIXMATSIZE
from PSFOTFTSC2 import PSFOTFTSC
from segpos2 import SEGPOS
from ATTOS_FWHM2 import ATTOS_FWHM
from COOGRID2 import COOGRID
from PSD_ANISO_SERVO_GLAO_STAR3  import PSD_ANISO_SERVO_GLAO_STAR
import random
import readallnew

import time



'''################################################主函数###########################################################'''


# lam_path =  '/home/lab30202/lcf/GaussianMixtureModel/data/paranal/all/'
# sordar_path = '/home/lab30202/lcf/GaussianMixtureModel/data/sordardata/'
# ali_path = '/home/lab30202/lcf/GaussianMixtureModel/data/ali/allprofs/'
# massdata_path = '/home/lab30202/lcf/GaussianMixtureModel/data/mass/'
#
# x1 = readallnew.read(lam_path,sordar_path,ali_path,massdata_path)
# # x1.readmassdata()
# # profdata = x1.prodata_mass
# # filename = x1.timedata
# x1.readlapalmadata()
# profdata = x1.prodata
# filename = x1.proname






def paola(MODE,DIM,TSC,W0,L0,ZA,HEIGHT,DISTCN2,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21=None,P22=None,\
          DISPERSION=None,FWHM_ANALYSIS=None,INFO=1,PSF=1,OTF=1,SF=1,PSD=None,ONLY_PSD=1,ANTI_ALIAS=None,SCINTILLATION=None, FITSCODE=None,SINGLE=None,LOGCODE='star1',\
          X_PSF=None,Y_PSF=None,PRECISION=None,OPTIMIZE_WFS_INT=None,OPTIMIZE_LOOP_GAIN=None,OPTIMIZE_ALL=None,POST_TIPTILT=None,TILT_ANGLE_STEP=None,FRFFT=None):

    '''n_params函数'''
    # n_params=n_param([MODE,DIM,TSC,W0,L0,ZA,HEIGHT,DISTCN2,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22])
    n_params = 20


    '''GLAO MODE'''
    if MODE.lower() == 'glao' :
        if PRECISION == None :
            PRECISION = 'double'
            # SETTING VARIABLES ACCORDING TO MODE
        if MODE.lower() == 'seli' and n_params() == 9 :
            WIND=P09
        if MODE.lower() == 'ngs' :
            WIND = P09
            DM_HEIGHT = P10['dm_height']
            ACTPITCH = P10['actpitch']
            DMTF = P10['dmtf']
            WFS_PITCH = P11['wfs_pitch']
            GS_ANG = P12
            GS_ORI = P13
            WFS_INT = P14
            LAG = P15
            LOOP_MODE = P16
            LOOP_GAIN = P17
            if n_params() == 20 :
                MIRVEC = P11['MIRVEC']
                NBLENSES = P11['NBLENSES']
                EXTRAFILTER = P11['EXTRAFILTER']
                WFS_RON = P11['WFS_RON']
                ALGORITHM = P11['ALGORITHM']
                if ALGORITHM.lower() == 'cg' :
                    WFS_JITTER = P11['WFS_JITTER']
                    WFS_PXFOV = P11['WFS_PXFOV']                                                              #long类型对应？
                    WFS_PXSIZE = P11['WFS_PXSIZE']

                NGS_MAG = P18
                FILTER = P19.lower()
                NGS_TEM = P20

            else :
                WFS_NEA = P18

        if MODE.lower() == 'glao' :
            if n_params == 13 :
                DM_HEIGHT = P09['dm_height']
                ACTPITCH = P09['actpitch']
                DMTF = P09['dmtf']
                WFS_PITCH = P10['wfs_pitch']
                GS_ANG = P11
                GS_ORI = P12
                GLAO_WFS = P13

            if n_params == 20 or n_params == 22 :
                WIND = P09
                DM_HEIGHT = P10['dm_height']
                ACTPITCH = P10['actpitch']
                DMTF = P10['dmtf']
                WFS_PITCH = P11['wfs_pitch']
                GS_ANG = P12
                GS_ORI = P13
                WFS_INT = P14
                LAG = P15
                LOOP_MODE = P16
                if LOOP_MODE.lower() == 'closed' :
                    messagebox.showinfo('warning', 'CLOSED LOOP NOT IMPLEMENTED IN GLAO MODE, YET. SORRY. SET LOOP MODE TO ''OPEN'' FOR NOW.')
                LOOP_GAIN = P17
                GLAO_WFS = P18
                GS_WEIGHT = P19
            if n_params == 20 :
                WFS_NEA=P20
            if n_params == 22 :
                MIRVEC = P11['MIRVEC']
                NBLENSES = P11['NBLENSES']
                EXTRAFILTER = P11['EXTRAFILTER']
                WFS_RON = P11['WFS_RON']
                ALGORITHM = P11['ALGORITHM']
                if ALGORITHM.lower() == 'cg' :
                    WFS_JITTER = P11['WFS_JITTER']
                    WFS_PXFOV = P11['WFS_PXFOV']
                    WFS_PXSIZE = P11['WFS_PXSIZE']

                NGS_MAG = P20
                FILTER = P21.lower()
                NGS_TEM = P22


        # HANDLING OUTER SCALE
        if L0 >10000 and INFO ==None :
            print('***********WARNING: OUTER SCALE LARGER THAN 10 KM. CONSIDERED INFINITE.')
        if L0 > 10000 :
            L0 =-1

        if WFS_INT != None :
            gsint=float(WFS_INT)
        if LOOP_GAIN != None :
            loopgain=float(LOOP_GAIN)
        if MODE.lower() == 'glao' :
            if GLAO_WFS['type'].lower() !='star' :
                gsint=0

        rad2asec = 3600.0 * 180.0/pi
        asec2rad = 1.0 / rad2asec
        W0rad = W0 * asec2rad
        r0500 = 0.98* 0.5e-6 / W0rad * cos(float (ZA) / 180 *pi) ** (3.0/ 5)
        r0LAM = r0500 * (DIM['LAMBDA'] / 0.5) ** (1.2)

        if L0 == -1 :
            aos=1
        if L0 != -1 :
            aos=(ATTOS_FWHM(TSC['DEXTMAX']/ r0LAM, TSC['DEXTMAX']/L0))

        if n_params > 6 :
            tmp = DISTCN2 / total(DISTCN2)
            w = (tmp>0)
            if not w.any() == False :
                newdistcn2 = tmp[w]
                newheight = HEIGHT[w] / cos(float(ZA) / 180.0 *pi)
                if not (MODE.lower() == 'glao' and n_params == 13) :
                    newwindx = (reform(WIND[0,:],[]))[w]
                    newwindy = (reform(WIND[1,:],[]))[w]
                    newwind = np.array([newwindx, newwindy])
            else:
                newdistcn2 = tmp
                newheight = HEIGHT / cos(float(ZA) / 180 *pi)
                if not (MODE.lower() == 'glao' and n_params == 13) :
                    newwind=WIND
        if n_params > 6 :
            cn2dh_i = (500.0e-9/2/pi)**2 /0.423* r0500**(-5.0 / 3) * newdistcn2
            r0500_i = r0500 * newdistcn2 ** (-3.0/5)

        if n_params > 6:
            meanalti = total(newdistcn2 * abs(newheight) ** (5.0 / 3)) ** (3.0 / 5)
            if meanalti != 0 :
                anisoang=0.314 / meanalti * r0500 * (DIM['LAMBDA'] / 0.5) ** (1.2) * rad2asec
            if meanalti == 0 :
                anisoang=0.0

        if n_params > 6 :
            if not (MODE.lower() == 'glao' and n_params == 13) :
                if newwind.any() != None :
                    meanwind = total(newdistcn2 * ((newwind[0,:] ** 2 + newwind[1,:] ** 2)**0.5) ** (5.0/3)) ** (3.0/5)
                    if meanwind != 0 :
                        timescal=0.314 / meanwind * r0500 * (DIM['LAMBDA'] / 0.5) ** (1.2) * 1000.0
                    if meanwind == 0 :
                        timescal=0
                else :
                    meanwind = newwind
                    if meanwind != 0 :
                        timescal=0.314/ meanwind * r0500 * (DIM['LAMBDA'] / 0.5) ** (1.2) * 1000.0
                    if meanwind == 0 :
                        timescal=0

        if MODE.lower() != 'seli' :
            ACTPITCHnom = r0LAM;
            if ACTPITCH == -1 :
                ACTPITCH=ACTPITCHnom
                dm_nactnom=TSC['DEXTMAX'] / ACTPITCHnom
                dm_nact=TSC['DEXTMAX'] / ACTPITCH
                if WFS_PITCH == -1 :
                    WFS_PITCH=ACTPITCH




        if PRECISION.lower()  == 'single' :
            xpcoohf=(COOGRID(DIM['N_OTF'], DIM['N_OTF'], SCALE=DIM['N_OTF']/2*DIM['DXP'], FT=1, RADIUS=1, SINGLE=1))['r']
        if PRECISION.lower()  == 'double' :
            xpcoohf=(COOGRID(DIM['N_OTF'], DIM['N_OTF'], SCALE=DIM['N_OTF']/2*DIM['DXP'], FT=1, RADIUS=1))['r']


        if PRECISION.lower()  == 'single' and MODE.lower() != 'seli' :
            fpcoolf=(COOGRID(DIM['N_LF'], DIM['N_LF'], SCALE=(DIM['N_LF']-1) / 2 * DIM['DFP_LF'], COO_X=1, SINGLE=1))['x']
        if PRECISION.lower()  == 'double' and MODE.lower() != 'seli' :
            fpcoolf=(COOGRID(DIM['N_LF'], DIM['N_LF'], SCALE=(DIM['N_LF']-1) / 2 * DIM['DFP_LF'], COO_X=1))['x']
        if PRECISION.lower()  == 'single' :
            fpcoohf=(COOGRID(DIM['N_OTF'], DIM['N_OTF'], SCALE=DIM['N_OTF']/ 2 * DIM['DFP'], FT=1, COO_X=1, SINGLE=1))['x']
        if PRECISION.lower()  == 'double' :
            fpcoohf=(COOGRID(DIM['N_OTF'], DIM['N_OTF'], SCALE=DIM['N_OTF']/ 2 * DIM['DFP'], FT=1, COO_X=1))['x']

        if MODE.lower() != 'seli':
            if PRECISION.lower() == 'single' :
                if not (type(DMTF) is np.ndarray):
                    FTMD=(abs(fpcoolf) <= (1+1e-3) * 0.5/ ACTPITCH) & (abs(np.rot90(fpcoolf, 3)) <= (1+1e-3) * 0.5/ ACTPITCH)
                if (type(DMTF) is np.ndarray):
                    FTMD=float(DMTF)
            else:
                if not (type(DMTF) is np.ndarray):
                    FTMD=(abs(fpcoolf) <= (1+1e-3) * 0.5 / ACTPITCH) & (abs(np.rot90(fpcoolf, 3)) <= (1+1e-3) * 0.5/ ACTPITCH)
                if (type(DMTF) is np.ndarray):
                    FTMD=DMTF

        #var = np.zeros(shape=int(4))


        if DISPERSION == None :
            DISPERSION = 1


        '''Fitting error PSD'''
        #tmp = PSD_HFERR_NGS(DIM['N_OTF'],fpcoohf,r0LAM,float(L0),0,WFS_PITCH,PRECISION)
        #Whf = tmp
        #var[0] = 0.2313 * (WFS_PITCH / r0LAM) ** (5.0 / 3)
        if strlowcase(PRECISION) == 'single' :
            Wlf=np.zeros(shape=(int(DIM['N_LF']), int(DIM['N_LF'])))
        if strlowcase(PRECISION) == 'double' :
            Wlf=np.zeros(shape=(int(DIM['N_LF']), int(DIM['N_LF'])))
        '''WFS aliasing PSD'''
        #if ANTI_ALIAS == None and GLAO_WFS['type'] == 'star' :
        #   if gsint == None :
        #        tmp = DISPERSION ** 2 * PSD_ALIAS_NGS_GLAO(DIM['N_LF'], fpcoolf, DIM['LAMBDA'], newheight, [[0], [0]],r0500, float(L0), 0, WFS_PITCH, FTMD, DM_HEIGHT, 0,GS_WEIGHT, GLAO_WFS, PRECISION)
        #    else:
        #        tmp = DISPERSION ** 2 * PSD_ALIAS_NGS_GLAO(DIM['N_LF'], fpcoolf, DIM['LAMBDA'], newheight, newwind, r0500_i,float(L0), 0, WFS_PITCH, FTMD, DM_HEIGHT, gsint,GS_WEIGHT, GLAO_WFS, PRECISION)

        #    if PSD != None or ONLY_PSD != None :
        #        Walias = tmp
        #    Wlf = Wlf + tmp
        #    var[1] = total(tmp) * DIM['DFP_LF'] ** 2

        '''aniso-servo PSD'''
        if GLAO_WFS['type'] == 'star' :
            if n_params == 13 :
                tmp = PSD_ANISO_SERVO_GLAO_STAR(DIM['N_LF'], fpcoolf, DIM['LAMBDA'], newheight,dblarr(n_elements(newheight), 2), r0500_i, float(L0), WFS_PITCH, FTMD,DM_HEIGHT,GS_ANG,GS_ORI,0,0,GS_WEIGHT,GLAO_WFS,PRECISION)
            if n_params != 13:
                tmp = PSD_ANISO_SERVO_GLAO_STAR(DIM['N_LF'], fpcoolf, DIM['LAMBDA'], newheight, newwind, r0500_i, float(L0),WFS_PITCH, FTMD,DM_HEIGHT, GS_ANG, GS_ORI, gsint, LAG, GS_WEIGHT, GLAO_WFS, PRECISION)
        if PSD != None or ONLY_PSD != None :
            Wanisoservo = tmp
        Wlf = Wlf + tmp
        #var[2] = total(tmp) * DIM['DFP_LF'] ** 2
        var = total(tmp) * DIM['DFP_LF'] ** 2
        '''WFS noise PSD'''
        #if strlowcase(GLAO_WFS['type']) == 'star' :
        #    tmp = np.zeros(shape=(int(DIM['N_LF']), int(DIM['N_LF'])))
        # if NGS_MAG != None :
        #     nstar=n_elements(NGS_MAG)
        #if WFS_NEA.any() != None :
        #    nstar=n_elements(WFS_NEA)
        #if n_elements(GS_WEIGHT) == 1 :
        #    gsw=np.zeros(shape=(int(nstar))) +1.0 / nstar
        #if n_elements(GS_WEIGHT) != 1 :
        #    gsw=GS_WEIGHT

        #  WFS noise PSD from the GS magnitudes and spectrums and RON
           # if NGS_MAG != None :
           #     pass  #具体功能暂不写

        #WFS noise PSD from GS Noise Equivalent Angle
        #if WFS_NEA.any() != None :
        #    tmp = PSD_NOISE_NGS_GLAO(DIM['N_LF'], fpcoolf, WFS_PITCH, FTMD, gsw, WFS_NEA, DIM['LAMBDA'], PRECISION)
        #   if PSD != None or ONLY_PSD != None :
        #        Wnoise = tmp
        #    Wlf = Wlf + tmp
        #    var[3] = total(tmp) * DIM['DFP_LF'] ** 2

        return var













