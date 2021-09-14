# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
from Myproblem import MyProblem # 导入自定义问题接口
import random
import readallnew
import matplotlib.pyplot as plt
plt.get_backend()
plt.switch_backend('agg')




if __name__ == '__main__':
    """===============================读取廓线数据==========================="""
    lam_path = '/home/lab30202/lcf/GaussianMixtureModel/data/paranal/all/'
    sordar_path = '/home/lab30202/lcf/GaussianMixtureModel/data/sordardata/'
    ali_path = '/home/lab30202/lcf/GaussianMixtureModel/data/ali/allprofs/'
    massdata_path = '/home/lab30202/lcf/GaussianMixtureModel/data/mass/'

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
        Efield = []
        with open("/home/lab30202/lcf/class_test3/ga_results/paranalall_lgs5.txt", 'r') as file_to_read:
            # 判断是否已经计算过
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                site = lines[52:84]  # 5lgs paranal data
                # site= lines[52:71]    #5lgs  mass
                # site= lines[42:74]      #4lgs
                # site= lines[32:61]    #3lgs
                Efield.append(site)
                if not lines:
                    break
            pass
        if str(filenames) in Efield:
            continue
        else:
            hcn2data = profdata[indx].reshape((100, 4))
            atmlist = np.ones([100, 4])
            # atmlist[:, 0] = hcn2data[:, 0]
            # prodatacn2 = np.log10(hcn2data[:, 1] + 1)  # paranal data
            # atmlist[:, 1] = (prodatacn2 - min(prodatacn2)) / (max(prodatacn2) - min(prodatacn2))
            atmlist = hcn2data


            
    if __name__ == '__main__':
        """================================实例化问题对象==========================="""
        problem = MyProblem(atmlist) # 生成问题对象
        """==================================种群设置==============================="""
        Encoding = 'RI'       # 编码方式
        NIND = 20            # 种群规模
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
        population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """================================算法参数设置============================="""
        myAlgorithm = ea.soea_DE_rand_1_bin_templet(problem, population) # 实例化一个算法模板对象
        myAlgorithm.MAXGEN = 100 # 最大进化代数
        myAlgorithm.mutOper.F = 0.5 # 差分进化中的参数F
        myAlgorithm.recOper.XOVR = 0.7 # 重组概率
        """===========================调用算法模板进行种群进化======================="""
        [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
        population.save() # 把最后一代种群的信息保存到文件中
        # 输出结果
        best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
        best_ObjV = obj_trace[best_gen, 1]
        print('最优的目标函数值为：%s'%(best_ObjV))
        print('最优的决策变量值为：')
        for i in range(var_trace.shape[1]):
            print(var_trace[best_gen, i])
        print('有效进化代数：%s'%(obj_trace.shape[0]))
        print('最优的一代是第 %s 代'%(best_gen + 1))
        print('评价次数：%s'%(myAlgorithm.evalsNum))
        print('时间已过 %s 秒'%(myAlgorithm.passTime))

