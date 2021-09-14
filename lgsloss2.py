from numpy import cos, pi

lgs_list1 = [366.0509, 1.8336, 363.3720, 2.6308, 360.5462, 4.8634, 360.1746, 5.6313, 361.1192, 3.7426]
lgs_list2 = [361.8020, 1.9153, 363.8925, 1.1870, 360.0654, 3.1484, 360.6320, 5.0754, 360.4963, 4.3103]


def star_L(lgs1, lgs2):
    # 求两个点之间的距离
    r1 = lgs1[0]
    angle1 = lgs1[1]
    r2 = lgs2[0]
    angle2 = lgs2[1]
    L = (r1 ** 2 + r2 ** 2 - 2 * r1 * r2 * cos(angle1 / pi - angle1 / pi)) ** 0.5
    return L

def sort(dir):
    # 按照距离将对应星排序,l矩阵中存放各对应星之间的距离；location矩阵中，存放对应的星
    for i in range(len(dir['l'])):
        for j in range(i+1,len(dir['l'])):
            if dir['l'][j] < dir['l'][i]:
                temp = dir['l'][j]
                dir['l'][j] = dir['l'][i]
                dir['l'][i] = temp

                temp = dir['location'][j]
                dir['location'][j] = dir['location'][i]
                dir['location'][i] = temp

    return dir

def replace():
    pass



def lgsloss(lgs_list1, lgs_list2):

    match_star1 = {'l': [], 'location': []}
    match_star2 = {'l': [], 'location': []}
    match_star3 = {'l': [], 'location': []}
    match_star4 = {'l': [], 'location': []}
    match_star5 = {'l': [], 'location': []}

    matchdir = {
        "star1": match_star1,
        "star2": match_star2,
        "star3": match_star3,
        "star4": match_star4,
        "star5": match_star5
    }

    lgs_List1 = [star11, star12, star13, star14, star15] = [lgs_list1[:2], lgs_list1[2:4], lgs_list1[4:6],
                                                            lgs_list1[6:8], lgs_list1[8:10]]
    lgs_List2 = [star21, star22, star23, star24, star25] = [lgs_list2[:2], lgs_list2[2:4], lgs_list2[4:6],
                                                            lgs_list2[6:8], lgs_list2[8:10]]

    numi = 0
    for i in lgs_List1:
        numi = numi + 1
        numj = 0
        for j in lgs_List2:
            numj = numj + 1
            matchdir["star" + str(numi)]['l'].append(star_L(i, j))
            matchdir["star" + str(numi)]['location'].append(str(numj))
            matchdir["star" + str(numi)] = sort(matchdir["star" + str(numi)])

    # print(matchdir)
    #　如果害怕极端情况可以加一个五重循环，但是应该没有必要
    for ni in range(1,6):
        for nj in range(ni+1,6):
            if matchdir["star" + str(ni)]['location'][0] == matchdir["star" + str(nj)]['location'][0]:
                if matchdir["star" + str(ni)]['l'][0] > matchdir["star" + str(nj)]['l'][0]:
                    # temp = matchdir["star" + str(ni)]['l'][0]
                    for k in range(len(matchdir["star" + str(ni)]['l'])-1):
                        matchdir["star" + str(ni)]['l'][k] = matchdir["star" + str(ni)]['l'][k+1]
                        matchdir["star" + str(ni)]['location'][k] = matchdir["star" + str(ni)]['location'][k+1]
                else :
                    for k in range(len(matchdir["star" + str(nj)]['l'])-1):
                        matchdir["star" + str(nj)]['l'][k] = matchdir["star" + str(nj)]['l'][k+1]
                        matchdir["star" + str(nj)]['location'][k] = matchdir["star" + str(nj)]['location'][k+1]

    result = 0.0
    for i in range(1,6):
        result += matchdir["star" + str(i)]['l'][0]

    return result



# lgsloss(lgs_list1, lgs_list2)
# for k in range(len(a["star" + str(5)]['l']),0,-1):
#     print(a["star" + str(5)]['l'][k-1])
#     print(k)

print(lgsloss(lgs_list1, lgs_list2))

