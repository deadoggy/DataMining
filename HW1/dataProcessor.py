#coding:utf-8

import pandas
import math


class dataProcessor:

    __mFileName = 'Traj_1000_SH_UTM'
    __originX = 346000
    __originY = 3448600
    __endX = 362800
    __endY = 3463800
    __width = 840
    __height = 760
    __gridWidth = 20
    __inf = 1000000000
    def readFile(self):
        #从文件读取数据
        data = pandas.read_csv(self.__mFileName)

        #获取数据的数量
        dataSize = len(data.X)

        #把数据处理成栅格类型
        dataAfterProcessToGrid = []

        minGridIndex = self.__inf
        maxGridIndex = -1;

        for index in range(dataSize):
            '''
                栅格的尺寸是840 × 760
                计算栅格的序号，公式为：
                grid = [ width × (Y - originY )+(X - originY) ] / 20
            '''

            grid = ( self.__width * ( data.Y[index] - self.__originY ) + (data.X[index] - self.__originX) ) / self.__gridWidth

            grid = math.floor(grid)

            minGridIndex = grid if grid < minGridIndex else minGridIndex

            maxGridIndex = grid if grid > maxGridINdex else maxGridIndex

            dataAfterProcessToGrid.append([data.Tid[index], data.Time[index], grid ])

        #缩小grid的序号的范围
        for index in range(dataSize):
            dataAfterProcessToGrid[index][2] - minGridIndex

        #返回轨迹矩阵和dataframe
        return  [ maxGridIndex - minGridIndex, dataAfterProcessToGrid ]






if __name__ == '__main__':
    testObj = dataProcessor()

    testObj.readFile()
