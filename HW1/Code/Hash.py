#coding: utf-8

from dataProcessor import *
from lshash import lshash as ls


class HashData:

    def __init__(self, mDataProcessor = None):

        print "Initiallizing......"

        if mDataProcessor is None:
            dP = dataProcessor()
        else:
            dP = mDataProcessor

        self.__originData = dP.gridData
        self.__data = dP.dataFrame
        self.__hashSizeList = [10, 11, 12, 13, 14, 15]
        self.__traceToCheckList = [15, 250, 480, 690, 900]

        self.__hashProcessors = {}
        inputDim = len(self.__originData[0])

        #对于每一种hash_size
        for size in self.__hashSizeList:
        #只用10测试
        # for size in [10]:
            lsh = ls.LSHash(size, inputDim)
            #把每个向量分别输入到hash_table中
            for index in range(dP.getTraceSum()):
                input_point = self.__data.iloc[:, index].tolist()
                lsh.index(input_point, extraData(index, self.__originData[2][index][1], self.__originData[2][index][2])) #额外数据是轨迹的开始时间和结束时间
            #把每个处理器存入类变量
            self.__hashProcessors[size] = lsh

        print "Initialization Success!"

    def run(self):
        print "Running...."

        ret = {}
        for sizeOpt in self.__hashSizeList:
            ret[sizeOpt] = []
            for trace in self.__traceToCheckList:
                query_point = self.__data[trace-1].tolist()
                result = self.__hashProcessors[sizeOpt].query(query_point, 100, "hamming")
                ret[sizeOpt].append([trace, result])# result 中 tid比

        return ret




if __name__ == "__main__":

    print "start"

    for tableSize in range(1, 11):
        print "table size:" + str(tableSize) + '\n'
        print "///////////////////////////////////////////////////"
        print "///////////////////////////////////////////////////"

        test = HashData(tableSize)
        test.run()
