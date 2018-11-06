# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/10/21'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import operator
import pickle
from math import log
import matplotlib.pyplot as plt


def calcShannonEnt(dataSet):
    """
    计算给定数据集的香浓熵
    :param dataSet:
    :return:
    """
    # 计算实例的总数
    numEntries = len(dataSet)
    # 构造类别计数字典，计算出每个类别出现的次数
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    # print(shannonEnt)
    return shannonEnt


def creatDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


# calcShannonEnt(myDat)


def splitDataSet(dataSet, axis, value):
    """
    按照给定特征划分数据集
    :param dataSet:
    :param axis:
    :param value:
    :return:
    """
    
    retDataset = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis]
            reduceFeatVec.extend(featVec[axis + 1:])
            retDataset.append(reduceFeatVec)
    return retDataset


def chooseBestFeatureToSplit(dataSet):
    """
    选择最好的数据集划分方式
    :param dataSet:
    :return:
    """
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featlist = [example[i] for example in dataSet]
        uniqueVals = set(featlist)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    """
    统计类次数，并且返回出现次数最多的类别
    :param classList:
    :return:
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# def createTree(dataSet,labels):
#     classList = [example[-1] for example in dataSet]
#     if classList.count(classList[0]) == len(classList):
#         return classList[0]
#     if len(dataSet[0]) == 1:
#         return majorityCnt(classList)
#     bestFeat = chooseBestFeatureToSplit(dataSet)
#     bestFeatlabel= labels[bestFeat]
#     myTree = {bestFeatlabel:{}}
#     del(labels[bestFeat])
#     featValues = [example[bestFeat] for example in dataSet]
#     uniqueVals = set(featValues)
#     for value in uniqueVals:
#         subLabels = labels[:]
#         myTree[bestFeatlabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
#
#     return  myTree

def createTree(dataSet, labels):
    # 获取数据集中的最后一列的类标签，存入classList列表
    classList = [example[-1] for example in dataSet]
    # 通过count()函数获取类标签列表中第一个类标签的数目
    # 判断数目是否等于列表长度，相同表面所有类标签相同，属于同一类
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # 遍历完所有的特征属性，此时数据集的列为1，即只有类标签列
    if len(dataSet[0]) == 1:
        # 多数表决原则，确定类标签
        return majorityCnt(classList)
    # 确定出当前最优的分类特征
    bestFeat = chooseBestFeatureToSplit(dataSet)
    # 在特征标签列表中获取该特征对应的值
    bestFeatLabel = labels[bestFeat]
    # 采用字典嵌套字典的方式，存储分类树信息
    myTree = {bestFeatLabel: {}}
    
    ##此位置书上写的有误，书上为del(labels[bestFeat])
    ##相当于操作原始列表内容，导致原始列表内容发生改变
    ##按此运行程序，报错'no surfacing'is not in list
    ##以下代码已改正
    
    # 复制当前特征标签列表，防止改变原始列表的内容
    subLabels = labels[:]
    # 删除属性列表中当前分类数据集特征
    del (subLabels[bestFeat])
    # 获取数据集中最优特征所在列
    featValues = [example[bestFeat] for example in dataSet]
    # 采用set集合性质，获取特征的所有的唯一取值
    uniqueVals = set(featValues)
    # 遍历每一个特征取值
    for value in uniqueVals:
        # 采用递归的方法利用该特征对数据集进行分类
        # @bestFeatLabel 分类特征的特征标签值
        # @dataSet 要分类的数据集
        # @bestFeat 分类特征的标称值
        # @value 标称型特征的取值
        # @subLabels 去除分类特征后的子特征标签列表
        myTree[bestFeatLabel][value] = createTree(splitDataSet \
                                                      (dataSet, bestFeat, value), subLabels)
    return myTree


decisionNode = dict(boxstyle='sawtooth', fc='0.8')
leafNode = dict(boxstyle='round4', fc='0.8')
arrow_args = dict(arrowstyle='<-')


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
                            va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)


# def createPlot():
#     fig = plt.figure(1,facecolor='white')
#     fig.clf()
#     createPlot.ax1 = plt.subplot(111,frameon=False)
#     plotNode('decitionNode',(0.5,0.1),(0.1,0.5),decisionNode)
#     plotNode('leafNode', (0.8, 0.1), (0.3, 0.8), leafNode)
#     plt.show()


def getNumleafs(mytree):
    numLeafs = 0
    firstStr = list(mytree.keys())[0]
    secondDict = mytree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumleafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(mytree):
    maxDepth = 0
    firstStr = list(mytree.keys())[0]
    secondDict = mytree[firstStr]
    for key in secondDict:
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    
    return maxDepth


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    # 如果子节value是字典型则该节点是决策节点，否则是叶子节点
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xoff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yoff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yoff = plotTree.yoff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xoff = plotTree.xoff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xoff, plotTree.yoff), cntrPt, leafNode)
            plotMidText((plotTree.xoff, plotTree.yoff), cntrPt, str(key))
    plotTree.y0ff = plotTree.yoff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumleafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xoff = -0.5 / plotTree.totalW
    plotTree.yoff = 1.0
    
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


def classify(inputTree, featLabels, testVec):
    # 找到树的第一个分类特征，或者说根节点'no surfacing'
    # 注意python2.x和3.x区别，2.x可写成firstStr=inputTree.keys()[0]
    # 而不支持3.x
    firstStr = list(inputTree.keys())[0]
    # 从树中得到该分类特征的分支，有0和1
    secondDict = inputTree[firstStr]
    # 根据分类特征的索引找到对应的标称型数据值
    # 'no surfacing'对应的索引为0
    featIndex = featLabels.index(firstStr)
    # 遍历分类特征所有的取值
    for key in secondDict.keys():
        # 测试实例的第0个特征取值等于第key个子节点
        if testVec[featIndex] == key:
            # type()函数判断该子节点是否为字典类型
            if type(secondDict[key]).__name__ == 'dict':
                # 子节点为字典类型，则从该分支树开始继续遍历分类
                classLabel = classify(secondDict[key], featLabels, testVec)
            # 如果是叶子节点，则返回节点取值
            else:
                classLabel = secondDict[key]
    return classLabel


def storeTree(inputTree, filename):
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    fr = open(filename, 'rb')
    return pickle.load(fr)


myDat, labels = creatDataSet()
mytree = createTree(myDat, labels)
# storeTree(mytree,'classifierStorage.txt')
grabTree('classifierStorage.txt')


def glassTest():
    # 打开文本数据
    fr = open('lenses.txt')
    # 将文本数据的每一个数据行按照tab键分割，并依次存入lenses
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    # 创建并存入特征标签列表
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    # 根据继续文件得到的数据集和特征标签列表创建决策树
    lensesTree = createTree(lenses, lensesLabels)
    return lensesTree


t = glassTest()
createPlot(t)



