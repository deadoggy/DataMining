#coding:utf-8

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import numpy as np
import math

class Predictor:

    def __init__(self, alg, dataSource):
        '''

        :param alg: 算法 cla / reg
        '''
        self.alg = alg
        self.testX = []
        self.testYLL = []
        self.testYG = []
        self.trainX = []
        self.trainYLL = []
        self.trainYG = []
        self._loadData(dataSource)

    def _loadData(self, dataSource):
        '''
        把数据加载到内存
        :param dataSource: 数据种类 : gsm / lte
        :return:
        '''
        if "gsm" == dataSource:
            pre = "gsm_data/"
        elif "lte" == dataSource:
            pre = "lte_data/"
        else:
            print "unknown data source"
            raise Exception("unknown data source")
        self.testX = self.__fromFileLoadList(pre + "testX")
        self.testYLL = self.__fromFileLoadList(pre + "testYLL")
        self.testYG = self.__fromFileLoadList(pre + "testYG")
        self.trainX = self.__fromFileLoadList(pre + "trainX")
        self.trainYLL = self.__fromFileLoadList(pre + "trainYLL")
        self.trainYG = self.__fromFileLoadList(pre + "trainYG")

    def __fromFileLoadList(self, fileName):
        '''
        从文件中读取一个list
        :param fileName: 文件名
        :return: 一个list
        '''
        ret = []
        file = open(fileName, 'r')
        line = file.readline()
        while len(line) > 0:
            splitLine = line.split(" ")
            temp = []
            for item in splitLine:
                temp.append(eval(item))
            if 1 == len(temp):
                ret.append(temp[0])
            else:
                ret.append(temp)
            line = file.readline()
        return ret

    def fit(self):
        '''
        训练并预测
        :return:
        '''

        #根据算法选择分类器还是回归
        if 'cla' == self.alg:
            predictor = RandomForestClassifier(n_estimators=30)
            trainY = self.trainYG
            Y = self.testYG
        else:
            predictor = RandomForestRegressor(n_estimators=30)
            trainY = self.trainYLL
            Y = self.testYLL

        predictor.fit(self.trainX, trainY)
        predRes = predictor.predict(self.testX)
        correctRate =  predictor.score(self.testX, Y)

        if 'cla' == self.alg: #如果是分类其返回正确率
            return correctRate
        else: #如果是回归返回平均误差
            div = (predRes - Y) * (predRes - Y)
            return np.mean( np.sqrt(div[:, 0] + div[:, 1]) )




if __name__ == "__main__":
    # obj = Predictor("cla", "lte")
    # obj.fit()
    #
    obj = Predictor("reg", "lte")
    print obj.fit()

