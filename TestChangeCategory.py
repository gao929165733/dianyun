import numpy as np
from laspy.file import File
import time


inFile = File("./tests/demo1.las", mode="rw")
# 指定修改类别
Category = 6
# 选定区域点坐标
# regional_point = [['454466.6800', '2870746.4997', '1662.5400'], ['454505.1200', '2870688.4997', '1661.7300'], ['454539.3700', '2870764.7497', '1651.1800']]
# regional_point = [['454592.2800','2870658.9997','1663.7200'], ['454569.9600','2870631.9997','1666.2600'], ['454646.8400','2870615.7497','1663.5700'], ['454621.7100','2870587.9997','1675.1600']]

# 更改指定区域点云类别
# i[0][0]-x i[0][1]-y i[0][2]-z i[0][5]-class
def changeCategory(regional_point):
    start = time.time()
    the_list = dotRange(regional_point)
    num = 0
    for i in inFile.points:
        if the_list[0]<= scaled_x_dimension(i[0][0]) <= the_list[1] and the_list[2]<= scaled_y_dimension(i[0][1]) <= the_list[3] and the_list[4]<= scaled_z_dimension(i[0][2]) <= the_list[5]:
            i[0][5] = Category
        else:
            continue
    end = time.time()
    print(end-start)
    print(the_list)

# 测试
def test1(regional_point):
    the_list = dotRange(regional_point)
    start = time.time()
    for i in inFile.points:
        if the_list[0]<= scaled_x_dimension(i[0][0]) <= the_list[1] and the_list[2]<= scaled_y_dimension(i[0][1]) <= the_list[3] and the_list[4]<= scaled_z_dimension(i[0][2]) <= the_list[5]:
            print(i[0][5])
    end = time.time()
    print(end - start)

def test2(regional_point):
    start = time.time()
    the_list = dotRange(regional_point)
    num = 0
    for i in inFile.points:
        continue
    end = time.time()
    print(end-start)

# x坐标转化
def scaled_x_dimension(x_coordinate):
    scale = inFile.header.scale[0]
    offset = inFile.header.offset[0]
    convertCoord = x_coordinate * scale + offset
    return convertCoord

# y坐标转化
def scaled_y_dimension(y_coordinate):
    scale = inFile.header.scale[1]
    offset = inFile.header.offset[1]
    convertCoord = y_coordinate * scale + offset
    return convertCoord

# z坐标转化
def scaled_z_dimension(z_coordinate):
    scale = inFile.header.scale[2]
    offset = inFile.header.offset[2]
    convertCoord = z_coordinate * scale + offset
    return convertCoord

# 坐标范围点
# [x_min,x_max,y_min,y_max,z_min,z_max]
def dotRange(regional_point):
    the_list = [0] * 6
    list_x = []
    list_y = []
    list_z = []
    for singleDot in regional_point:
        list_x.append(eval(singleDot[0]))
        list_y.append(eval(singleDot[1]))
        list_z.append(eval(singleDot[2]))

    the_list[0] = sorted(list_x)[0]
    the_list[1] = sorted(list_x)[-1]
    the_list[2] = sorted(list_y)[0]
    the_list[3] = sorted(list_y)[-1]
    the_list[4] = sorted(list_z)[0]
    the_list[5] = sorted(list_z)[-1]
    return the_list


if __name__=="__main__":

    regional_point = [['454598.1200','2870677.9997','1658.5800'], ['454587.4300','2870644.9997','1665.5600'], ['454630.7100','2870643.7497','1661.9000']]
    # regional_point = ['454592.2800', '2870658.9997', '1663.7200'], ['454569.9600', '2870631.9997', '1666.2600'],
    # ['454646.8400', '2870615.7497', '1663.5700']
    changeCategory(regional_point)
    # test(regional_point)
    # test2(regional_point)
    pass
