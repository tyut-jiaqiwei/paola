
from function import *
from math import pi


def err_exit(FUN=0,ERR=0):
    if  not(isinstance(FUN,str)) or not(isinstance(ERR,str)):
        return
    else:
        print('#############################')
        print('ERROR IN THE FUNCTION/PROCEDURE : '+FUN)
        print('ERROR MESSAGE : '+ERR)
        print('#############################')



def SEGPOS(FIRST_INPUT=None,DINT=None):

    DEXT = FIRST_INPUT
    NSD = 1
    GAP = 0
    TYPE = 'DISC'

    pos=np.zeros(shape=(1,2))

    tns=1

    if TYPE.upper()  == 'DISC':
        swd = float(DEXT)
        ssz = 0.5*float(DEXT)
        dbs = 0.0

    if TYPE.upper()  == 'DISC' :
        surf=tns*pi*ssz**2
    if tns == 1 :
        surf=surf-pi*(0.5*DINT)**2


    if TYPE.upper()  == 'DISC' :
        dextmax=2*ssz

    dxy = np.zeros(shape=(2, int(tns)))

    result={'TNS':tns,'SWD':swd,'SSZ':ssz*2,'DBS':dbs,'POS':pos,'DEXTMAX':dextmax,'DEXT':DEXT,'DINT':DINT,'TYPE':TYPE,'GAP':GAP,'NSD':NSD,'SURF':surf,'REMSEG':'n'}

    return(result)

