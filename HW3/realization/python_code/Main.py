#coding:utf-8

from DataProcessor import DataProcessor
from Predictor import Predictor
import matplotlib.pyplot as plt
import numpy as np

class Main:

    def generateData(self, rate):
        obj = DataProcessor(0)
        obj.loadFileAndRetrieveCh()
        obj.saveToFile(rate)

        obj = DataProcessor(1)
        obj.loadFileAndRetrieveCh()
        obj.saveToFile(rate)

    def runAlg(self, dataType):
        '''
        运行算法的函数，并且画图
        :param dataType: gsm / lte
        :return:
        '''
        if dataType != "gsm" and dataType != "lte":
            raise Exception("未知数据类型")

        #分类器和回归器的结果
        regRes = []
        claRes = []

        predorCla = Predictor("cla", dataType)
        predorReg = Predictor("reg", dataType)
        for time in range(10):
            print str(time) + " -- begin"

            #跑算法
            claRes.append(predorCla.fit())
            regRes.append(predorReg.fit())
            print str(time) + " -- change data"
            # 重新生成一个数据的划分
            predorReg.changeData()
            predorCla.changeData()

        #排序
        regRes.sort()
        claRes.sort()

        folder = "gsmResult/" if "gsm" == dataType else "lteResult/"

        #画图
        self.draw(regRes, folder+"regImg")
        self.draw(claRes, folder+"claImg")

        #输出结果和中位结果
        resFile = open(folder+"res", 'w')
        resFile.write("reg result:\n")
        resFile.write(str(regRes))
        resFile.write("\nreg mid:\n")
        resFile.write(str((regRes[4] + regRes[5]) / 2))

        resFile.write("\ncla result:\n")
        resFile.write(str(claRes))
        resFile.write("\ncla mid:\n")
        resFile.write(str((claRes[4] + claRes[5]) / 2))

    def draw(self, res, imgName):

        plt.plot(res)
        plt.savefig(imgName)
        plt.close()

if __name__ == "__main__":
    obj = Main()
    obj.runAlg("gsm")
    obj.runAlg("lte")
