from numpy import cos,pi

lgs_list1 =[366.0509,   1.8336, 363.3720,   2.6308, 360.5462,   4.8634, 360.1746, 5.6313, 361.1192,   3.7426]
lgs_list2 =[361.8020,   1.9153, 363.8925,   1.1870, 360.0654,   3.1484, 360.6320, 5.0754, 360.4963,   4.3103]

def star_L(lgs1,lgs2):
    # 求两个点之间的距离
    r1     = lgs1[0]
    angle1 = lgs1[1]
    r2     = lgs2[0]
    angle2 = lgs2[1]
    L      = (r1**2 + r2**2 - 2*r1*r2*cos(angle1/pi - angle1/pi))**0.5
    return L

def lgsloss(lgs_list1,lgs_list2):

    star = {'l':[],'location':None}

    matchdir = {
        "star1": {'l': [], 'rank': None},
        "star2": {'l': [], 'rank': None},
        "star3": {'l': [], 'rank': None},
        "star4": {'l': [], 'rank': None},
        "star5": {'l': [], 'rank': None}
    }

    lgs_List1 = [star11, star12,star13,star14,star15] = [lgs_list1[:2], lgs_list1[2:4],lgs_list1[4:6],lgs_list1[6:8],lgs_list1[8:10]]
    lgs_List2 = [star21, star22, star23, star24, star25] = [lgs_list2[:2], lgs_list2[2:4], lgs_list2[4:6], lgs_list2[6:8],lgs_list2[8:10]]

    numi = 0
    for i in lgs_List1 :
        numi = numi + 1
        numj = 0
        for j in lgs_List2 :
            numj = numj + 1
            matchdir["star" + str(numi)]['l'].append(star_L(i,j))
        matchdir["star" + str(numi)]['l'].sort(reverse=True)
        matchdir["star" + str(numi)].append(str(numj))
            ### 还是不行，实在不行的话添加字典





        if matchdir["star" + str(numi)] == matchdir["star" + str(numi-1)]:
            if matchdir["star" + str(numi)] < matchdir["star" + str(numi-1)]:
                for k in range(len(matchdir["star" + str(numi)])-1):
                    matchdir["star" + str(numi)][k+1] = matchdir["star" + str(numi)][k]
            else:
                for k in range(len(matchdir["star" + str(numi-1)])-1):
                    matchdir["star" + str(numi-1)][k+1] = matchdir["star" + str(numi-1)][k]


        #





    # 如果lgslist1的星全部接近lgslist2中的某个星，只有最接近的那个星才可以匹配该星，其他匹配该星的星自动后移
