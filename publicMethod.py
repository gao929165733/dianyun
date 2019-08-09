import os


# 创建目录
def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已存在')
        return False


inputFormatC = ["xyz", "rgb", "i"]
outputFormatC = ["BINARY", "LAS", "LAZ"]
outputAttributesC = ["RGB", "INTENSITY", "CLASSIFICATION"]

# potree转化
def converter(converterCmd, the_input, page, the_output, inputFormat, outputFormat, outputAttributes, overwrite):
    # 输入文件路径存在
    if(os.path.exists(the_input) == True):
        print("vivld input")
        converterCmd = converterCmd + " " + the_input
    else:
        print("wrong input")
        return False
    # 文件输出路径存在
    if(os.path.exists(the_output) == True):
        print("vivld output")
        converterCmd = converterCmd + " -o " + the_output
    else:
        print("wrong output")
        return False
    # page不为空 要求生成html文件
    if(page != None):
        converterCmd = converterCmd + " -p " + page
    if(inputFormat != None):
        converterCmd = converterCmd + " -f " + inputFormatC[inputFormat]

    if(outputFormat != None):
        converterCmd = converterCmd + " --output-format " + outputFormatC[outputFormat]

    if(outputAttributes != None):
        converterCmd = converterCmd + " -a " + outputAttributesC[outputAttributes]

    if(overwrite != None and overwrite == True):
        converterCmd = converterCmd + " --overwrite "
    print(converterCmd)
    os.system(converterCmd)
    return True


def segRoot(the_path):
    the_path = the_path.split('\\')
    print(the_path)
    the_path = the_path[-1]
    return the_path


# las文件合并
def LASmerge(input, output):
    mergeCmd = "G:\\A点云workplace\\lastools\\master\\bin\\lasmerge.exe"
    # 当前路径为文件目录
    if(os.path.exists(input)):
        print("vivld input")
        mergeCmd = mergeCmd + " -i " + input + "\\*.las" + " -o " + output
        # 执行命令
        os.system(mergeCmd)
        if(os.path.exists(output)):
            return True
        else:
    	    return False
    else:
        return False

# txtToJson
import json
import chardet
def wayTxtToJson(input, output):
    jsonList = []
    # try:
    with open(input, mode='r') as txtFile:
        lines = txtFile.readlines()
    keys = ['ID', 'section', 'distance', 'x', 'y', 'z', 'class', 'horDis', 'verDis', 'airDis']
    for line in lines[1:]:
        num = lines.index(line)
        line = line.replace('\t', ' ').rstrip().split(' ')
        line.insert(0, num)
        the_dic = dict(zip(keys, line))
        jsonList.append(the_dic)
    with open(output, mode='w+', encoding='utf-8') as jsonFile:
        json.dump(jsonList, jsonFile, ensure_ascii=False)
    return True

# 交跨点
def wayTXTcrossfile(input):
    jsonList = []
    with open(input, mode='r') as txtFile:
        lines = txtFile.readlines()
    keys = ['ID', 'section', 'distance', 'x', 'y', 'z', 'class', 'horDis', 'verDis', 'airDis']
    for line in lines[1:]:
        num = lines.index(line)
        line = line.replace('\t', ' ').rstrip().split(' ')
        line.insert(0, num)
        the_dic = dict(zip(keys, line))
        jsonList.append(the_dic)
    print(jsonList)
    return jsonList

# 危险点
def wayTXTdangerfile(input):
    jsonList = []
    with open(input, mode='r') as txtFile:
        lines = txtFile.readlines()
    keys = ['ID', 'section', 'distance', 'x', 'y', 'z', 'class', 'horDis', 'verDis', 'airDis']
    for line in lines[1:]:
        num = lines.index(line)
        line = line.replace('\t', ' ').rstrip().split(' ')
        line.insert(0, num)
        the_dic = dict(zip(keys, line))
        jsonList.append(the_dic)
    print(jsonList)
    return jsonList

# 杆塔
def wayTXTtowerfile(input):
    jsonList = []
    with open(input, mode='r') as txtFile:
        lines = txtFile.readlines()
    keys = ['ID', 'X', 'Y', 'Z_min', 'Z_max']
    for line in lines[1:]:
        num = str(lines.index(line)) + '#'
        line = line.replace('\t', ' ').rstrip().split(' ')
        line.insert(0, num)
        the_dic = dict(zip(keys, line))
        jsonList.append(the_dic)
    print(jsonList)
    return jsonList


if __name__ == "__main__":
    # the_path = r'G:\python\the_dianyun\static\projects\asd'
    # print(segRoot(the_path))
    # converter(converterCmd, r'C:\Users\92916\Desktop\text.file\demo.las', '', r'G:\python\the_dianyun\project\text1', None, 1, None, None)
    # LASmerge('G:\\python\\the_dianyun\\static\\projects\\1\data\\r','G:\python\\the_dianyun\\static\\projects\\1\\3.las')
    # print('end')
    # input = r'C:\Users\92916\Desktop\交跨点列表_2018-08-17-13-40-38.txt'
    # output = r'C:\Users\92916\Desktop\交跨点列表_2018-08-17-13-40-38.json'
    # wayTxtToJson(input, output)
    # input = r'C:\Users\92916\Desktop\测试.txt'
    pass