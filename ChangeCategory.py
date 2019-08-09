import numpy as np
from laspy.file import File
import time


inFile = File("./tests/demo1.las", mode="rw")

# 更改指定区域点云类别
# i[0][0]-x i[0][1]-y i[0][2]-z i[0][5]-class
def changeCategory(regional_point):
    start = time.time()
    the_list = dotRange(regional_point)
    # 坐标转换
    XYZ_list = scaled_XYZ_dimension(the_list)
    for i in inFile.points:
        for j in the_list:
            # 在区域类的点坐标
            if j[1] <= i[0][0] <= j[2] and j[3] <= i[0][1] <= j[4] and j[5] <= i[0][2] <= j[6]:
                i[0][5] = j[0] # 改变类别
                # print(i[0][5])
                continue
    end = time.time()
    print(end-start)
    return True

# XYZ坐标转换
def scaled_XYZ_dimension(the_list):
    # 比例和偏移值
    print(the_list)
    scale = inFile.header.scale
    offset = inFile.header.offset
    for j in the_list:
        j[1] = round((j[1] - offset[0]) / scale[0])
        j[2] = round((j[2] - offset[0]) / scale[0])
        j[3] = round((j[3] - offset[1]) / scale[1])
        j[4] = round((j[4] - offset[1]) / scale[1])
        j[5] = round((j[5] - offset[2]) / scale[2])
        j[6] = round((j[6] - offset[2]) / scale[2])
    print(the_list)
    return the_list


# X坐标转化
def scaled_X_dimension(X_coordinate):
    scale = inFile.header.scale[0]
    offset = inFile.header.offset[0]
    convertCoord = (X_coordinate - offset) / scale
    convertCoord = round(convertCoord)
    print(convertCoord)
    return convertCoord

# Y坐标转化
def scaled_Y_dimension(Y_coordinate):
    scale = inFile.header.scale[1]
    offset = inFile.header.offset[1]
    convertCoord = (Y_coordinate - offset) / scale
    convertCoord = round(convertCoord)
    return convertCoord

# Z坐标转化
def scaled_Z_dimension(Z_coordinate):
    scale = inFile.header.scale[2]
    offset = inFile.header.offset[2]
    convertCoord = (Z_coordinate - offset) / scale
    convertCoord = round(convertCoord)
    return convertCoord


# 坐标范围点
def dotRange(regional_point):
    the_list = []
    # 点数据集合
    for singleRePoint in regional_point:

        # print(singleRePoint)

        the_single_list = []# 一次类别改变数据
        list_x = [] # 存储x点数据
        list_y = [] # 存储y点数据
        list_z = [] # 存储z点数据
        # 单独的点数据
        for singleDot in singleRePoint:
            # 第一个为类别
            if len(singleDot) < 3:
                theClass = eval(singleDot[0])
                continue
            # 点数据
            list_x.append(eval(singleDot[0]))
            list_y.append(eval(singleDot[1]))
            list_z.append(eval(singleDot[2]))
        # [theClass,x_min,x_max,y_min,y_max,z_min,z_max]
        the_single_list.append(theClass)
        the_single_list.append(sorted(list_x)[0])
        the_single_list.append(sorted(list_x)[-1])
        the_single_list.append(sorted(list_y)[0])
        the_single_list.append(sorted(list_y)[-1])
        the_single_list.append(sorted(list_z)[0])
        the_single_list.append(sorted(list_z)[-1])
        # [[the_single_list], [the_single_list]]
        the_list.append(the_single_list)
    # print(the_list)
    return the_list


if __name__=="__main__":

    regional_point = [

        [['7'], ['454472.1200', '2870832.4997', '1636.7300'], ['454450.5900', '2870829.7497', '1668.2800'],
         ['454450.6800', '2870791.7497', '1647.7900'], ['454478.2400', '2870795.4997', '1647.1600']],
        [['6'], ['454601.6200', '2870673.9997', '1658.0800'], ['454586.5900', '2870649.9997', '1665.4100'],
         ['454626.6200', '2870639.9997', '1662.7800']],
        [['5'], ['454590.1200', '2870616.7497', '1670.9300'], ['454569.6200', '2870585.7497', '1683.7000'],
         ['454610.6800', '2870576.9997', '1681.5200']]

    ]

    # the_list = dotRange(regional_point)
    changeCategory(regional_point)
    # scaled_X_dimension(454499.8700)
    # scaled_XYZ_dimension(the_list)

    pass
