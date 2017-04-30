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

        self.testX = []
        self.testYLL = []
        self.testYG = []
        self.trainX = []
        self.trainYLL = []
        self.trainYG = []


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
                X = self.testX
                YLL = self.testYLL
                YG = self.testYG
            else:
                CSV = csv.reader(trainOriginData)
                X = self.trainX
                YLL = self.trainYLL
                YG = self.trainYG
            for index, line in enumerate(CSV):
                # 跳过表头
                if 0 == index:
                    continue
                # 特征值
                ch = [eval(line[2]), eval(line[3])]
                # 信号强度
                for stationIndex in range(6):
                    ch.append(eval(line[11 + stationIndex]))  # 服务网络控制器
                    ch.append(eval(line[12 + stationIndex]))  # 基站
                    ch.append(eval(line[14 + stationIndex]) - eval(line[13 + stationIndex]))  # 信号强度
                X.append(ch)
                # 栅格Y
                YG.append(eval(line[47]))
                # 经纬Y
                YLL.append([eval(line[9]), eval(line[10])])
        testOriginData.close()
        trainOriginData.close()

    def saveToFile(self):
        '''
        把特征值数据存入文件
        :return:
        '''
        #test数据
        testXFile = open(self.outFolder+"testX", 'w')
        for item in self.testX:
            for chItem in item:
                testXFile.write(str(chItem) + " ")
            testXFile.write("\n")
        testXFile.close()

        testYGFile = open(self.outFolder+"testYG", 'w')
        for item in self.testYG:
            testYGFile.write(str(item) + "\n")
        testYGFile.close()

        testYLLFile = open(self.outFolder+"testYLL", 'w')
        for item in self.testYLL:
            for llItem in item:
                testYLLFile.write(str(llItem) + " ")
            testYLLFile.write("\n")
        testYLLFile.close()


        #train数据
        trainXFile = open(self.outFolder+"trainX",'w')
        for item in self.trainX:
            for chItem in item:
                trainXFile.write(str(chItem) + " ")
            trainXFile.write("\n")
        trainXFile.close()

        trainYGFile = open(self.outFolder+"trainYG", 'w')
        for item in self.trainYG:
            trainYGFile.write(str(item) + "\n")
        trainYGFile.close()

        trainYLLFile = open(self.outFolder+"trainYLL", 'w')
        for item in self.trainYLL:
            for llItem in item:
                trainYLLFile.write(str(llItem) + " ")
            trainYLLFile.write("\n")
        trainYLLFile.close()


if __name__ == "__main__":
    obj = DataProcessor(0)
    obj.loadFileAndRetrieveCh()
    obj.saveToFile()

    obj = DataProcessor(1)
    obj.loadFileAndRetrieveCh()
    obj.saveToFile()
