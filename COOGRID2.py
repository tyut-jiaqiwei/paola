
from function import *
import time
import numpy as np

def COOGRID(NX,NY,SCALE=None,FT=None,XMIN=None,XMAX=None,YMIN=None,YMAX=None,SINGLE=None,COO_X=None,COO_Y=None,RADIUS=None ,ANGLE=None):

    start = time.time()

    if typeof(XMIN) == None:
        if FT != None:
            x_int = np.arange(NX).reshape(1,int(NX)) * 2.0 / NX - 1.0
            y_int = np.arange(NY).reshape(1,int(NY)) * 2.0/ NY - 1.0
        else:
            x_int = np.arange(NX).reshape(1,int(NX)) * 2.0 / (NX - 1) - 1.0
            y_int = np.arange(NY).reshape(1,int(NY)) * 2.0 / (NY - 1) - 1.0
        if SCALE != None:
            x_int = x_int * SCALE
            y_int = y_int * SCALE
    else:
        x_int = np.arange(NX).reshape(1,int(NX)) * (XMAX - XMIN) / (NX - 1) + XMIN
        y_int = np.arange(NY).reshape(1,int(NY)) * (YMAX - YMIN) / (NY - 1) + YMIN

    tout = int(0)
    if not ((COO_X != None) or (COO_Y != None) or (RADIUS != None) or (ANGLE != None)) :
        tout = int(1)

    if ((COO_X != None ) or (RADIUS != None) or (ANGLE != None) or tout) :
        if SINGLE == None:
            x_mat = np.zeros(shape=(int(NX),int(NY))) #dblarr和fltarr的区别是？
        if SINGLE != None:
            x_mat = np.zeros(shape=(int(NX),int(NY)))  #目前两者没有设置区别
        x_mat=np.dot(np.ones([int(NY),1]),x_int)

    if  COO_Y == None or RADIUS == None or ANGLE == None or tout :
        if SINGLE == None :
            y_mat = np.zeros(shape=(int(NX),int(NY)))
        if SINGLE != None:
            y_mat = np.zeros(shape=(int(NX),int(NY)))
        y_mat=np.dot((y_int).T,np.ones([1,int(NX)]))

    if  RADIUS != None or ANGLE != None or tout:
        if SINGLE == None :
            r_mat = np.zeros(shape=(int(NX),int(NY)))
        if SINGLE != None:
            r_mat = np.zeros(shape=(int(NX),int(NY)))
        r_mat = (x_mat**2 + y_mat**2)**0.5


    if ANGLE != None or tout:
        if SINGLE == None :
            t_mat = np.zeros(shape=(int(NX),int(NY)))
        if SINGLE != None:
            t_mat = np.zeros(shape=(int(NX),int(NY)))
        w = where(r_mat,'gt',0)
        t_mat[w] = acos(x_mat[w]/r_mat[w])  #找到acos对应的函数


    # 结果
    if tout:
        return {'x': x_mat, 'y': y_mat, 'r': r_mat, 't': t_mat}
    if COO_X != None:
        result = {'x':x_mat}
        if COO_Y != None:
            result = create_struct(result, 'y', y_mat)
            if RADIUS != None:
                result = create_struct(result, 'r', r_mat)
                if ANGLE != None:
                    result = create_struct(result, 't', t_mat)
            elif ANGLE != None:
                result = create_struct(result, 't', t_mat)
        else:
            if RADIUS != None:
                result = create_struct(result, 'r', r_mat)
                if ANGLE != None:
                    result = create_struct(result, 't', t_mat)
            elif ANGLE != None:
                result = create_struct(result, 't', t_mat)
    else:
        if COO_Y != None:
            result = create_struct('y', y_mat)
            if RADIUS != None:
                result = create_struct(result, 'r', r_mat)
                if ANGLE != None:
                    result = create_struct(result, 't', t_mat)
            elif ANGLE != None:
                result = create_struct(result, 't', t_mat)
        else:
            if RADIUS != None:
                result = {'r':r_mat}
                if ANGLE != None:
                    result = create_struct(result, 't', t_mat)
            elif ANGLE != None:
                result = {'t':t_mat}

    end = time.time()
    # print('COOGRID用时' + str(end-start) )

    return (result)











