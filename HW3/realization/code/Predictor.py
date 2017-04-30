#coding:utf-8

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

class Predictor:

    def __init__(self, type):
        if 0 == type:
            self.predictor = RandomForestClassifier(n_estimators=100)
        else:
            self.predictor = RandomForestRegressor(n_estimators=100)
        self.testX = []
        self.testYLL = []
        self.testYG = []
        self.trainX = []
        self.trainYLL = []
        self.trainYG = []

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
        self.testX = self.__fromFileLoadList(pre + "textX")
        self.testYLL = self.__fromFileLoadList(pre + "textYLL")
        self.testYG = self.__fromFileLoadList(pre + "testYG")
        self.trainX = self.__fromFileLoadList(pre + "trainX")
        self.trainYLL = self.__fromFileLoadList(pre + "trainYLL")
        self.trainYG = self.__fromFileLoadList(pre + "trainYG")

    def __fromFileLoadList(self, fileName):
        '''
        从文件中读取一个list
        :param fileName: 文件名
        :return:
        '''
        ret = []
        file = open(fileName, 'w')
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
        return ret