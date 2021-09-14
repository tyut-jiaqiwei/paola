import geatpy as ea
import numpy as np
import multiprocessing as mp
from numpy import pi,sin,cos,exp
import eva

class MyProblem(ea.Problem): # 继承Problem父类
    def __init__(self,atmlist):
        self.atmlist = atmlist
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 12 # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = np.zeros(12) # 决策变量下界
        ub = np.array([420,6,420,6,420,6,420,6,420,6,420,6]) # 决策变量上界
        lbin = np.ones(12) # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = np.ones(12) # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)



    def aimFunc(self, pop): # 目标函数
        Phen = pop.Phen
        x1 = np.array([Phen[:, 0]]).T
        y1 = np.array([Phen[:, 1]]).T
        x2 = np.array([Phen[:, 2]]).T
        y2 = np.array([Phen[:, 3]]).T
        x3 = np.array([Phen[:, 4]]).T
        y3 = np.array([Phen[:, 5]]).T
        x4 = np.array([Phen[:, 6]]).T
        y4 = np.array([Phen[:, 7]]).T
        x5 = np.array([Phen[:, 8]]).T
        y5 = np.array([Phen[:, 9]]).T
        x6 = np.array([Phen[:,10]]).T
        y6 = np.array([Phen[:,11]]).T

        x = np.hstack([x1, x2, x3, x4, x5, x6])
        y = np.hstack([y1, y2, y3, y4, y5, y6])


        lgslist = np.zeros([20, 2, 6])
        for i in range(y.shape[0]):
            lgslist[i] = [x[i]*(sin(2*pi/6*y[i])),x[i]*(cos(2*pi/6*y[i]))]

        lgslist0=np.hstack([x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6])
        lgslist1=np.reshape(lgslist0,(lgslist0.shape[0],6,2))


        fov = 420
        atmlist = self.atmlist
        aperture = 10
        lgsheight = 90000


        # pool = mp.Pool(16)  # 多进程
        # results = [pool.apply_async(eva.eva, args=(lgslist[i].T, fov, atmlist, aperture)) for i in range(lgslist.shape[0])]
        # output = [p.get() for p in results]
        # pool.close()
        # pool.join()
        # pop.ObjV = np.array(output).reshape(-1, 1)

        results = [eva.eva(lgslist[i].T, fov, atmlist, aperture) for i in range(lgslist.shape[0])]
        pop.ObjV = np.array(results).reshape(-1, 1)
        
