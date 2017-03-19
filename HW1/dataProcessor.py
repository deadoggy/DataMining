#coding:utf-8

import pandas
import utm
import numpy as np
import matplotlib.pylab as plt


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
    __data = pandas.read_csv(__fileName)

    def __init__(self):
        self.gridData = self._readFile()
        self.dataFrame = self._tansferDataToGridMatrix(self.gridData)

    def _readFile(self):
        #从文件读取数据
        data = self.__data

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

    def _tansferDataToGridMatrix(self, paraDataMatrix):

        retMatrix = pandas.DataFrame(0, paraDataMatrix[0], range(self.__traceSum))

        for point in paraDataMatrix[1]:
            retMatrix.loc[point[2], point[0]-1] = 1

        return retMatrix

    def drawTrace(self, tid = None, saveName = "All"):




        traceItemX = []
        traceItemY = []
        dataSize = len(self.__data.X)
        # 对于所有轨迹数据
        for index in range(dataSize):
            # tid 是空 或者 当前轨迹在tid中, 就打印该轨迹
            if tid is None or self.__data.Tid[index] in tid:
                latX, latY = utm.to_latlon(self.__data.X[index], self.__data.Y[index], 51, northern=True)
                traceItemX.append(latX)
                traceItemY.append(latY)

                # 最后一个数据点, 打印轨迹并清空轨迹记录列表
                if index == dataSize - 1 or self.__data.Tid[index] != self.__data.Tid[index + 1]:
                    plt.plot(traceItemX, traceItemY)
                    traceItemX = []
                    traceItemY = []

        #保存
        plt.xticks(np.linspace(31.16, 31.30, 8))
        plt.yticks(np.linspace(121.376, 121.560, 10))
        plt.savefig("Result/Img/"+saveName+".png")
        plt.close('all')

    def getTraceSum(self):
        return self.__traceSum




