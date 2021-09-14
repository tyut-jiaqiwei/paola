
from numpy import pi,sin,cos,exp

from function import *
from COOGRID2 import COOGRID
from DISCFT2 import DISCFT
from MATHFT2 import MATHFT
import time

def PSFOTFTSC(MIR, DIM, DM_PARAMS=None, WFSPITCH=None, PMR=None, IMAGER=None, PUPIL=None, PHASE=None , PHASOR=None,INFO=None, SINGLE=None, ANTI_ALIAS=None , WFEMAP=None ):

    start = time.time()

    rad2asec = 3600.0 * 180.0 /pi
    asec2rad = 1.0 / rad2asec

    # FOCAL PLANE ANGULAR FREQUENCY COORDINATES [1/RAD]
    ffocx = (COOGRID(DIM['N_OTF'], DIM['N_OTF'], FT=1, SCALE=DIM['N_OTF']/2*DIM['DFF'], COO_X=1))['x']
    fpupx = (COOGRID(DIM['N_OTF'], DIM['N_OTF'], FT=1, SCALE=DIM['N_OTF']/2 * DIM['DFP'], COO_X=1))['x']
    fpupy = np.rot90(fpupx, 3)
    fpupr = (fpupx ** 2 + fpupy ** 2) ** 0.5

    # PUPIL PLANE COORDINATES (CENTERED ON DIM.N_OTF/2)
    xpupx = (COOGRID(DIM['N_OTF'], DIM['N_OTF'], FT=1, SCALE=DIM['N_OTF'] / 2 * DIM['DXP'], COO_X=1))['x']

    # LOGICAL TAGS TO CHECK FOR EXISTENCE OF SEGMENT ERRORS DATA AND SPIDER
    INDDZ = (tag_names(MIR)=='DZ').any() ==True
    INDTT = (tag_names(MIR)=='TT').any() ==True
    INDDX = (tag_names(MIR)=='DXY').any() ==True
    INDZE = (tag_names(MIR)=='ZERCOE').any() ==True
    SPI = (tag_names(MIR)=='ARM_WIDTH').any() ==True

    SYMETRIC = 0

    wpp = (MIR['POS'][:,0] > 0 ) & (MIR['POS'][:,1] >0)
    wpm = (MIR['POS'][:,0] > 0 ) & (MIR['POS'][:,1] <0)
    wmp = (MIR['POS'][:,0] < 0 ) & (MIR['POS'][:,1] >0)
    wmm = (MIR['POS'][:,0] < 0 ) & (MIR['POS'][:,1] <0)


    if MIR['TNS'] == 1:
        obt = MIR['DINT']
    if MIR['TNS'] > 1:
        obt = 0.0
    if strlowcase(MIR['TYPE']) == 'disc':
        tfseg = DISCFT(fpupx, fpupy, MIR['SSZ'], obt)
        # print(tfseg)
    elif strlowcase(MIR['TYPE']) == 'hexa':
        tfseg = HEXAFT(fpupx, fpupy, MIR['SSZ'], obt)
    elif strlowcase(MIR['TYPE']) == 'squa':
        tfseg = RECTFT(fpupx, fpupy, MIR['SSZ'], MIR['SSZ'], obt)

    tmp = np.full(shape=(int(DIM['N_OTF']),int(DIM['N_OTF'])),fill_value=complex(0,0))

    for indpos in range(MIR['TNS']):
        tmp=tmp+np.exp(dcomplex(1,0)*2*pi*MIR['POS'][indpos,0]*fpupx+MIR['POS'][indpos,1]*fpupy)
    phasor_0=tmp*tfseg
    # phaseFT 暂定为None
    phaseFT = None
    if typeof(phaseFT) != None :
        pass
    else:
        streh1=1.0
        tmp=MATHFT(abs(phasor_0)**2,IC=DIM['N_OTF']/2,JC=DIM['N_OTF']/2)
    otf = tmp/abs(tmp[int(DIM['N_OTF']/2), int(DIM['N_OTF']/2)])
    # if IMAGER != None :
    #     otf = otf * otfccd
    tmp = np.full(shape=(DIM['N_PSF_USR'], DIM['N_PSF_USR']), fill_value=complex(0,0))  # dcomplexarr
    #tmp[DIM['N_PSF_USR']/2 - DIM['N_OTF']/2:DIM['N_PSF_USR']/2+DIM['N_OTF']/2-1][DIM['N_PSF_USR']/2 - DIM['N_OTF']/2: DIM['N_PSF_USR']/2 + DIM['N_OTF']/2-1] = otf
    tmp=otf
    psf = abs(MATHFT(tmp, IC=DIM['N_PSF_USR']/2, JC=DIM['N_PSF_USR']/2,INVERSE=1))
    psf = psf / psf.max() * streh1


    if IMAGER != None :
        inst = 'IMAGER'
    else:
        inst = 'SPECTRO'

    if SINGLE == None :
        result = {'PSF':psf,'OTF':otf}
        if PUPIL != None :
            result = create_struct(result, 'PUPIL', abs(pupille))
        if PHASE != None :
            if sizetype(phaseFT) != 0 :
                result = create_struct(result, 'PHASE', float(pupille * phase))
                result = create_struct(result, 'PHASEFT', phaseFT)

    result = create_struct(result, 'STREHL', streh1)
    result = create_struct(result,  'INST', inst)
    result = create_struct(result, 'LAMBDA', DIM['LAMBDA'])
    result = create_struct(result, 'DEXTMAX', MIR['DEXTMAX'])
    result = create_struct(result, 'MIRROR', MIR)
    if SPI or PMR != None :
        pass
    #     result = create_struct(result, 'SURF', newmirsurf)
    else:
        result = create_struct(result, 'SURF', MIR['SURF'])

    result = create_struct(result, 'AO_ON_FLAG', int(0.0))

    end = time.time()
    # print('PSFOTFTSC用时'+str(end-start))

    return result


