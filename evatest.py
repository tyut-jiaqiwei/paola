from numpy import pi,sin,cos,exp
import numpy as np
from function import *
from PIXMATSIZE2 import PIXMATSIZE
from PSFOTFTSC2 import PSFOTFTSC
from segpos2 import SEGPOS
from PSD_ANISO_SERVO_GLAO_STAR3  import PSD_ANISO_SERVO_GLAO_STAR
import random
import readallnew
import time
from paola import paola
import os
import multiprocessing as mp
import threading


def eva(lgslist,fov, atmlist, aperture):


    height = atmlist[:, 0]
    dcn2 = atmlist[:, 1]
    windir = atmlist[:, 3]* pi / 180
    wind = np.zeros([2,100])
    # wind = np.zeros([2, 5])
    v = atmlist[:, 2]
    ang06 = lgslist

    #paola_start = time.time()



    dcn2 = dcn2 / sum(dcn2)
    vx = v * np.cos(windir)
    vy = v * np.sin(windir)
    wind[0:] = vx
    wind[1:] = vy
    w0 = 0.7
    L0 = 27.0
    ZA = 0

    ori1 = np.zeros(8)
    ori2 = np.ones(8) * 45
    ori3 = np.ones(8) * 90
    ori4 = np.ones(8) * 135
    ori5 = np.ones(8) * 180
    ori6 = np.ones(8) * 225
    ori7 = np.ones(8) * 270
    ori8 = np.ones(8) * 315

    ori = np.hstack([ori1, ori2, ori3, ori4, ori5, ori6, ori7, ori8])                   #science object off-axis angle [asec]
    ang = np.array([148.49, 210, 257.196, 296.98, 332.039, 363.73, 392.874, 420] * 8)   #science object position angle in deg/x-axis




    '''GLAO MODES'''
    '''we will use here a simple telescope architecture - just a monolithic mirror'''
    mir = SEGPOS(aperture,1.8) #SEGPOS函数
    dxf = -1
    n_psf = -1 # default value = such that FoV = 8 times seeing limited PSF FWHM
    lam =1.25
    wfspitch = -1 # means that WFS pitch = r0 @ lambda
    dmh = 0 # conjugation height of the DM, here pupil level
    dm_params={'dmtf':-1,'actpitch':-1,'dm_height':dmh}                                                     ####字典的键要不要用字符，IDL中不用，py中用
    wfs_params={'wfs_pitch':wfspitch}
    wfs_int=10
    lag=5 #loop time lag (WFS reading + DM commands calculation) in msec
    '''Here we have 6 stars on a circle of radius 60 arcsec'''
    FoVrad = fov   # [asec]
    #print('ang06='+str(2*pi/6*pi*np.array([0,1,2,3,4,5])))
    glao_wfs={'type':'star','ang':ang06}
    info=1


    # pool = mp.Pool(100)
    #
    # results = [pool.apply_async(calaimfuc, args=(mir, dxf, n_psf, lam, w0, L0, ZA, height, dcn2, wind,dm_params,wfs_params, wfspitch, dmh, ang[i], ori[i], wfs_int, lag,glao_wfs, info)) for i in range(ang.shape[0])]
    #
    # output = [p.get() for p in results]
    # pool.close()
    # pool.join()
    # f=np.array(output).reshape(-1,1).sum()
    paola_start = time.time()
    f = [calaimfuc(mir, dxf, n_psf, lam, w0, L0, ZA, height, dcn2, wind,dm_params,wfs_params, wfspitch, dmh, ang[i], ori[i], wfs_int, lag,glao_wfs, info) for i in range(ang.shape[0])]
    f = np.array(f).reshape(-1, 1).sum()
    paola_end = time.time()
    print('评价函数（PSD）程序总用时' + str(paola_end - paola_start))

    return f



def calaimfuc(mir, dxf, n_psf, lam, w0, L0, ZA, height, dcn2, wind,dm_params,wfs_params, wfspitch, dmh, ang, ori, wfs_int, lag,glao_wfs, info):

    paola_start = time.time()

    psg2 = PIXMATSIZE(mir, dxf, n_psf, lam, w0, L0, ZA, height, dcn2, wind, wfspitch, dmh, ang, ori, wfs_int, lag,
                      glao_wfs, info)
    # now we need the telescope OTF
    tsc = PSFOTFTSC(mir, psg2)
    # GLAO modeling, giving a NEA for the WFS noise error
    gs_weight = -1  # all NGS of the constellation are given the same weight
    wfs_nea = np.zeros(6) + 0.02  # WFS Noise Equivalent Angle / NGS, in asec
    # print("wfs_nea="+str(wfs_nea))

    glao_star1=paola('glao',psg2,tsc,w0,L0,ZA,height,dcn2,wind,dm_params,wfs_params,ang,ori,wfs_int,lag,'open',1,glao_wfs,gs_weight,wfs_nea,\
                  INFO=1,OTF=1,PSF=1,SF=1,ONLY_PSD=1,LOGCODE='star1')

    paola_end = time.time()
    #print('评价函数（PSD）程序总用时' + str(paola_end - paola_start))

    return glao_star1







# atmlist = np.array([[250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,3500,3750,4000,4250,4500,4750,5000, \
#                      5250, 5500,  5750,  6000,  6250,  6500,  6750,  7000,  7250,  7500,7750,  8000,8250,  8500,  8750,  9000,  9250,  9500,  9750, 10000, \
#                      10250, 10500, 10750, 11000, 11250, 11500, 11750, 12000, 12250, 12500,12750, 13000, 13250, 13500, 13750, 14000, 14250, 14500, 14750, 15000,\
#                      15250, 15500, 15750, 16000, 16250, 16500, 16750, 17000, 17250, 17500,\
#                      17750, 18000, 18250, 18500, 18750, 19000, 19250, 24000, 24250, 24500,\
#                      24750,     0,     0,     0,     0,     0,     0,     0,     0,     0,\
#                      0,     0,     0,     0,     0,     0,     0,     0,     0,     0],
#                     [5.781e-14, 2.049e-14, 9.398e-15, 1.493e-14, 7.930e-15, 1.440e-15, 3.704e-15,\
#                     3.014e-15, 2.471e-15, 2.216e-15, 2.332e-15, 3.127e-15, 2.391e-15, 1.654e-15,\
#                     2.205e-15, 2.345e-15, 1.744e-15, 1.169e-15, 7.218e-16, 2.748e-16, 9.485e-16,\
#                     1.134e-15, 7.880e-16, 4.952e-16, 3.900e-16, 2.847e-16, 2.371e-16, 2.002e-16,\
#                     1.452e-16, 6.931e-17, 9.618e-17, 1.208e-15, 2.320e-15, 3.553e-15, 4.835e-15,\
#                     5.581e-15, 5.241e-15, 4.900e-15, 6.584e-15, 8.368e-15, 1.293e-14, 1.956e-14,\
#                     2.618e-14, 3.276e-14, 3.368e-14, 3.460e-14, 2.645e-14, 1.296e-14, 2.826e-15,\
#                     2.639e-15, 2.452e-15, 2.265e-15, 1.744e-15, 1.070e-15, 6.513e-16, 8.122e-16,\
#                     9.730e-16, 1.134e-15, 8.285e-16, 3.591e-16, 6.884e-17, 9.437e-17, 1.199e-16,\
#                     1.454e-16, 1.554e-16, 1.613e-16, 1.672e-16, 2.301e-16, 4.861e-16, 7.420e-16,\
#                     6.457e-16, 4.873e-16, 3.289e-16, 1.983e-16, 1.379e-16, 7.751e-17, 1.713e-17,\
#                     3.277e-17, 6.995e-17, 1.071e-16, 1.238e-16, 0.000e+00, 0.000e+00, 0.000e+00,\
#                     0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,\
#                     0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,\
#                     0.000e+00, 0.000e+00],
#                       [ 0.0  ,   0.0  ,   0.0   ,  0.0   ,  0.0  ,   0.0  ,   0.0  ,   0.0  ,   0.0  ,   0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0   ,  0.0  ,   0.0   ,  0.0  ,   0.0  ,   0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0  ,  0.0   ,  0.0  ,   0.0   ,  0.0  ,   0.0   ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  9.557 , 0.0   ,  0.0    , 0.0   ,  0.0    ,10.253 , 0.0,\
#                       0.0  ,   0.0  ,   0.0   , 16.225, 18.522, 19.789, 23.085 ,13.89 ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0  ,  16.663,  0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0  ,   0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0  ,   0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0  ,   0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0,\
#                       0.0  ,   0.0  ,   0.0   ,  0.0  ,   0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0   ,  0.0   ],
#                     [  0.0,    0.0,    0.0,    0.0,    0.0 ,   0.0 ,   0.0,    0.0,    0.0,    0.0,    0.0,    0.0,\
#                     0.0,    0.0,    0.0,    0.0,    0.0 ,   0.0,    0.0,    0.0,    0.0,    0.0,    0.0,    0.0,\
#                     0.0,    0.0,    0.0,    0.0,    0.0 ,   0.0 ,   0.0,    0.0,    0.0,  160.,    0.0 ,   0.0,\
#                     0.0,    0.0 , 255.7,   0.0 ,   0.0  ,  0.0 ,   0.0,  209.9 ,211.3 ,209.3, 208.6 ,250.5,\
#                     0.0 ,   0.0 ,   0.0,    0.0 ,   0.0 ,   0.0,  235.9,   0.0,    0.0 ,   0.0,    0.0,    0.0,\
#                     0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,  0.0  ,  0.0  ,  0.0,\
#                     0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0  ,  0.0 ,   0.0 ,   0.0 ,   0.0  ,  0.0 ,   0.0,\
#                     0.0 ,   0.0 ,   0.0 ,   0.0 ,   0.0  ,  0.0  ,  0.0 ,   0.0  ,  0.0  ,  0.0  ,  0.0  ,  0.0,\
#                     0.0 ,   0.0 ,   0.0 ,   0.0 ]
#                     ]).T




if __name__ == '__main__':
    """===============================读取廓线数据==========================="""
    lam_path = './data/paranal/all/'
    sordar_path = './data/sordardata/'



    ali_path = './data/ali/allprofs/'
    massdata_path = './data/mass/'

    x1 = readallnew.read(lam_path, sordar_path, ali_path, massdata_path)
    x1.readlapalmadata()
    profdata = x1.prodata
    filename = x1.proname

    for label in range(0, 1, 1):
        print("label=", label)
        indx = 1654
        #indx = random.choice(range(0, len(filename)))
        print("indx", indx)
        filenames = filename[indx]

        hcn2data = profdata[indx].reshape((100, 4))
        atmlist = np.ones([100, 4])
        # atmlist[:, 0] = hcn2data[:, 0]
        # prodatacn2 = np.log10(hcn2data[:, 1] + 1)  # paranal data
        # atmlist[:, 1] = (prodatacn2 - min(prodatacn2)) / (max(prodatacn2) - min(prodatacn2))
        atmlist = hcn2data


    # lgslist=np.array([[20.0*cos(2*pi/6*np.array([0,1,2,3,4,5]))],[20.0*sin(2*pi/6*np.array([0,1,2,3,4,5]))]]).T.reshape((6,2))
    lgslist = np.array([[0,296.985*cos(2 *pi/5*0),296.985*cos(2 *pi/5*1),296.985*cos(2 *pi/5*2),296.985*cos(2 *pi/5*3),296.985*cos(2 *pi/5*4)],
                        [0,296.985*sin(2 *pi/5*0),296.985*sin(2 *pi/5*1),296.985*sin(2 *pi/5*2),296.985*sin(2 *pi/5*3),296.985*sin(2 *pi/5*4),]]).T.reshape((6, 2))

    # lgslist = np.array([[0,420*cos(2*pi/5*0),420*cos(2*pi/5*1),420*cos(2*pi/5*2),420*cos(2*pi/5*3),420*cos(2*pi/5*4)],[0,420*sin(2*pi/5*0),420*sin(2*pi/5*1),420*sin(2*pi/5*2),420*sin(2*pi/5*3),420*sin(2*pi/5*4)]]).T.reshape((2,6))
    # print(lgslist)
    
    # atmlist = np.array([[1,1,1,1,1],[5,5,5,5,5],[0,0,0,0,0],[0,0,0,0,0]]).T

    fov = 420
    aperture = 10.0
    var = eva(lgslist,fov, atmlist, aperture)
    print(var)