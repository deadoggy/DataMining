#coding:utf-8

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import csv


class DataProcessor:

    def __init__(self, type):
        #GSM数据文件夹
        self.GSMDataFolder = "../GSM/"
        #GSM测试数据
        self.GSMTestDataFile = "new2gtest.csv"
        #GSM训练数据
        self.GSMTrainDataFile = "new2gtrain.csv"
        #LTE数据文件夹
        self.LTEDataFolder = "../LTE/"
        #LTE测试数据
        self.LTETestDataFile = "new4gtest.csv"
        #LTE训练数据
        self.LTETrainDataFile = "new4gtrain.csv"
        #输出数据文件夹
        self.outFolder = "gsm_data/" if 0 == type else "lte_data/"
        #类型
        self.type = type
        #特征中的基站数量
        self.station = 6

        self.X = []
        self.YLL = []
        self.YG = []


    def loadFileAndRetrieveCh(self):
        '''
        从文件里读入数据并提取特征值
        :return:
        '''

        if 0 == self.type:
            testOriginData = open(self.GSMDataFolder+self.GSMTestDataFile, 'r')
            trainOriginData = open(self.GSMDataFolder+self.GSMTrainDataFile, 'r')
        else:
            testOriginData = open(self.LTEDataFolder + self.LTETestDataFile, 'r')
            trainOriginData = open(self.LTEDataFolder + self.LTETrainDataFile, 'r')


        #提取特征
        for i in range(2): # 0是test数据, 1是train数据
            if 0 == i:
                CSV = csv.reader(testOriginData)
            else:
                CSV = csv.reader(trainOriginData)
            for index, line in enumerate(CSV):
                # 跳过表头
                if 0 == index:
                    continue
                # 特征值
                ch = [eval(line[2]), eval(line[3])]
                # ch = []
                # 信号强度
                for stationIndex in range(self.station):
                    # ch.append(eval(line[11 + stationIndex*6]))  # 服务网络控制器
                    # ch.append(eval(line[12 + stationIndex*6]))  # 基站
                    ch.append(eval(line[14 + stationIndex*6]) - eval(line[13 + stationIndex*6]))  # 信号强度
                self.X.append(ch)
                # 栅格Y
                self.YG.append(eval(line[47]))
                # 经纬Y
                self.YLL.append([eval(line[9]), eval(line[10])])
        testOriginData.close()
        trainOriginData.close()

    def saveToFile(self, rate):
        '''

        :param rate: 测试集占总数据的百分比
        :return:
        '''
        testX = []
        testYLL = []
        testYG = []
        trainX = []
        trainYLL = []
        trainYG = []

        testSum = int(rate *len(self.X))

        for index in range(len(self.X)):
            if index < testSum:
                testX.append(self.X[index])
                testYG.append(self.YG[index])
                testYLL.append(self.YLL[index])
            else:
                trainX.append(self.X[index])
                trainYLL.append(self.YLL[index])
                trainYG.append(self.YG[index])
        #test数据
        testXFile = open(self.outFolder+"testX", 'w')
        for item in testX:
            for index, chItem in enumerate(item):
                testXFile.write(str(chItem))
                if index != len(item)-1:
                    testXFile.write(" ")
            testXFile.write("\n")
        testXFile.close()

        testYGFile = open(self.outFolder+"testYG", 'w')
        for item in testYG:
            testYGFile.write(str(item) + "\n")
        testYGFile.close()

        testYLLFile = open(self.outFolder+"testYLL", 'w')
        for item in testYLL:
            for index, llItem in enumerate(item):
                testYLLFile.write(str(llItem))
                if index != len(item)-1:
                    testYLLFile.write(" ")
            testYLLFile.write("\n")
        testYLLFile.close()


        #train数据
        trainXFile = open(self.outFolder+"trainX",'w')
        for item in trainX:
            for index, chItem in enumerate(item):
                trainXFile.write(str(chItem))
                if index != len(item)-1:
                    trainXFile.write(" ")
            trainXFile.write("\n")
        trainXFile.close()

        trainYGFile = open(self.outFolder+"trainYG", 'w')
        for item in trainYG:
            trainYGFile.write(str(item) + "\n")
        trainYGFile.close()

        trainYLLFile = open(self.outFolder+"trainYLL", 'w')
        for item in trainYLL:
            for index, llItem in enumerate(item):
                trainYLLFile.write(str(llItem))
                if index != len(item)-1:
                    trainYLLFile.write(" ")
            trainYLLFile.write("\n")
        trainYLLFile.close()


if __name__ == "__main__":
    obj = DataProcessor(0)
    obj.loadFileAndRetrieveCh()
    obj.saveToFile(0.2)

    obj = DataProcessor(1)
    obj.loadFileAndRetrieveCh()
    obj.saveToFile(0.2)
