#coding: utf-8

from dataProcessor import *
from lshash import lshash as ls


class HashData:

    def __init__(self, hashTables):

        print "Initiallizing......"

        dP = dataProcessor()

        self.__originData = dP.readFile()
        self.__data = dP.tansferDataToGridMatrix(self.__originData)
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
        for sizeOpt in self.__hashSizeList:
            print "\nsize:" + str(sizeOpt) + '\n'
            for trace in self.__traceToCheckList:
                print "#######################################"
                print "query trace:" + str(trace) + '\n'
                query_point = self.__data[trace].tolist()
                result = self.__hashProcessors[sizeOpt].query(query_point, 100, "hamming")
                #输出结果
                for res in result:
                    if res[0][1].tid != trace:
                        print "result tid:" + str(res[0][1].tid)
                        print "start time:" + str(res[0][1].startTime)
                        print "end time:" + str(res[0][1].endTime)
                        print "distance:" + str(res[1]) + '\n'




if __name__ == "__main__":

    print "start"

    for tableSize in range(1, 11):
        print "table size:" + str(tableSize) + '\n'
        print "///////////////////////////////////////////////////"
        print "///////////////////////////////////////////////////"

        test = HashData(tableSize)
        test.run()
