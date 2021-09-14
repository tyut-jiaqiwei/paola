# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea # import geatpy
from Myproblem import MyProblem # 导入自定义问题接口
import random
import readallnew
import matplotlib.pyplot as plt
import json
import os
import csv
plt.get_backend()
plt.switch_backend('agg')


class SaveCSV(object):

    def save(self, keyword_list,path, item):
        """
        保存csv方法
        :param keyword_list: 保存文件的字段或者说是表头
        :param path: 保存文件路径和名字
        :param item: 要保存的字典对象
        :return:
        """
        try:
            # 第一次打开文件时，第一行写入表头
            if not os.path.exists(path):
                with open(path, "w", newline='', encoding='utf-8') as csvfile:  # newline='' 去除空白行
                    writer = csv.DictWriter(csvfile, fieldnames=keyword_list)  # 写字典的方法
                    writer.writeheader()  # 写表头的方法

            # 接下来追加写入内容
            with open(path, "a", newline='', encoding='utf-8') as csvfile:  # newline='' 一定要写，否则写入数据有空白行
                writer = csv.DictWriter(csvfile, fieldnames=keyword_list)
                writer.writerow(item)  # 按行写入数据
                print("^_^ write success")

        except Exception as e:
            print("write error==>", e)
            # 记录错误数据
            with open("error.txt", "w") as f:
                f.write(json.dumps(item) + ",\n")
            pass



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
        Efield = []
        with open("./ga_results/paranalall_lgs5.txt", 'r') as file_to_read:
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
            #print(atmlist.shape)
            #print(atmlist)


        """===============================实例化问题对象==========================="""
        problem = MyProblem(atmlist) # 生成问题对象
        """=================================种群设置==============================="""
        Encoding = 'BG'       # 编码方式
        NIND = 20             # 种群规模
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
        population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
        """===============================算法参数设置============================="""
        myAlgorithm = ea.soea_SEGA_templet(problem, population) # 实例化一个算法模板对象
        myAlgorithm.MAXGEN = 1 # 最大进化代数
        """==========================调用算法模板进行种群进化======================="""
        [population, obj_trace, var_trace] = myAlgorithm.run() # 执行算法模板
        population.save() # 把最后一代种群的信息保存到文件中
        # 输出结果
        best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
        best_ObjV = obj_trace[best_gen, 1]
        # print('最优的目标函数值为：%s'%(best_ObjV))
        # print('最优的控制变量值为：')
        # for i in range(var_trace.shape[1]):
        #     print(var_trace[best_gen, i])
        # print('有效进化代数：%s'%(obj_trace.shape[0]))
        # print('最优的一代是第 %s 代'%(best_gen + 1))
        # print('评价次数：%s'%(myAlgorithm.evalsNum))
        # print('时间已过 %s 秒'%(myAlgorithm.passTime))
        path = "%d.csv" % (indx)
        # 案例字典数据
        item = {'最优的目标函数值为':best_ObjV,'最优的决策变量值为':var_trace[best_gen, :], "有效进化代数":obj_trace.shape[0],"最优的一代":best_gen + 1,"评价次数": myAlgorithm.evalsNum, "时间已过":myAlgorithm.passTime}
        # 保存的表头
        item_list = [
            '最优的目标函数值',
            '最优的决策变量值',
            "有效进化代数",
            "最优的一代",
            "评价次数",
            "时间已过"
        ]

        s = SaveCSV()
        # 测试代码，循环写入三行，没有空行
        s.save(item_list, path, item)
