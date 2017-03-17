#coding:utf-8

import pandas
import time
import numpy as np


class extraData:

    def __init__(self, tid, startTime, endTime):
        self.tid = tid
        self.startTime = startTime
        self.endTime = endTime


class dataProcessor:

    __fileName = 'Traj_1000_SH_UTM'
    __originX = 346000
    __originY = 3448600
    __endX = 362800
    __endY = 3463800
    __width = 840
    __height = 760
    __gridWidth = 20
    __inf = 1000000000
    __traceSum = 1000

    def readFile(self):
        #从文件读取数据
        data = pandas.read_csv(self.__fileName)

        #获取数据的数量
        dataSize = len(data.X)

        #把数据处理成栅格类型
        dataAfterProcessToGrid = []

        #所有栅格的list
        gridList = []

        #trace 和 time的 list
        traceTime = []

        for index in range(dataSize):
            '''
                栅格的尺寸是840 × 760
                计算栅格的序号，公式为：
                grid =  width × [(Y - originY ) / 20] + [(X - originY)  / 20]
                注意所有数据取成int
            '''
            x = (data.X[index] - self.__originX)

            y = (data.Y[index] - self.__originY)

            grid = int(y/20) * self.__width + int(x/20)

            dataAfterProcessToGrid.append([data.Tid[index], data.Time[index], grid ])

            gridList.append(grid)

            #储存时间
            if 0 == len(traceTime) or 0 != cmp(traceTime[-1][0], data.Tid[index]):
                if len(traceTime) != 0:
                    traceTime[-1].append(data.Time[index-1])
                traceTime.append([data.Tid[index], data.Time[index]])

        traceTime[-1].append(data.Time[dataSize-1])

        unique_grid = np.unique(gridList)

        #返回 [ 所有栅格的列表, 数据[Tid, Time, GridIndex]  ]
        return  [ unique_grid, dataAfterProcessToGrid, traceTime]

    def tansferDataToGridMatrix(self, paraDataMatrix):

        retMatrix = pandas.DataFrame(0, paraDataMatrix[0], range(self.__traceSum))

        for point in paraDataMatrix[1]:
            retMatrix.loc[point[2], point[0]-1] = 1

        return retMatrix

    def getTraceSum(self):
        return self.__traceSum






if __name__ == "__main__":
    test = dataProcessor()
    test.readFile()