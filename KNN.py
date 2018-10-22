from numpy import *
import operator

import matplotlib.pyplot as plt


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ["A", "A", "B", "B"]
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    #     计算距离
    t = tile(inX,(dataSetSize,1))
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqdistance = sqDiffMat.sum(axis=1)
    distances = sqdistance ** 0.5
    
    sortedDistInDicies = distances.argsort()
    classCount = {}
    # 选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistInDicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVecotor = []
    index = 0
    
    # 解析文件到列表
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('\t')
        # 将每条数据前三个元素数据加入到数组的每一行
        returnMat[index, :] = listFromLine[0:3]
        classLabelVecotor.append(int(listFromLine[-1]))
        index += 1
    print(returnMat)
    return returnMat, classLabelVecotor


datingDataMat, datingLables = file2matrix("./datingTestSet2.txt")

# print(array(datingLables))

def datdShow():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2],15.0*array(datingLables),15.0*array(datingLables))
    plt.show()

def autoNorm(dataSet):
    """
    归一化数据，将数据转化为0-1之间的数值
    :param dataSet:
    :return:
    """
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals-minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet-tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals
# datdShow()

normMat,ranges,minVals = autoNorm(datingDataMat)
# print(minVals)


def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLables = file2matrix('./datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLables[numTestVecs:m], 3)
        print("the classifiler came back with : %d, the real answer is : %d" % (classifierResult, datingLables[i]))
        if (classifierResult != datingLables[i]):
            errorCount += 1.0
    print("the total number of errors is: %d" % errorCount)
    print("the total error rate is : %f" %(errorCount/float(numTestVecs)))
#
 
datingClassTest()
# group, labels = createDataSet()
# classify0([0,0],group,labels,3)