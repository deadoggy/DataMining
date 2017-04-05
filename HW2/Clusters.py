#coding: utf-8
import sklearn.cluster as cl
import pandas
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score

class Cluster:

    __dataFrame = pandas.DataFrame.from_csv("trace.csv")
    __npArrAfterPCA = []
    __originTraceData = []
    __initKCluster = 0
    __maxKCluster = -1

    def __init__(self, initK = None, maxK = None):

        #如果最大K比初始K小就Exception
        if initK is not None and maxK is not None and maxK < initK:
            raise Exception("initK bigger than maxK")

        originTraceFile = open("Traj_1000_SH_UTM")
        flag = -1

        # 读取文件第一行
        originTraceFile.readline()

        #从文件读取所有原始UTM坐标
        trace = []
        line = originTraceFile.readline()
        while len(line):
            line = line.split(",")
            Tid = eval(line[0])

            if Tid != flag:
                self.__originTraceData.append(trace)
                trace = []
                flag = Tid

            trace.append([eval(line[2]), eval(line[3])])
            line = originTraceFile.readline()

        self.__originTraceData.append(trace)

        #初始化最初的K
        self.__initKCluster = int((flag**0.5)/2) if initK is None else initK
        #初始化最大K
        self.__maxKCluster = flag if maxK is None else maxK

        #得出array 并且PCA降维
        self.__npArrAfterPCA = PCA().fit_transform(np.transpose(self.__dataFrame.__array__()))


    '''
       k-means 聚类

    '''
    def KMCluster(self):

        kList = range(self.__initKCluster, self.__maxKCluster+1)

        kAndSilCur = []

        silBest = -1

        for nCluster in kList:
            print nCluster
            # 生成一个聚类器
            clusterProcessor = cl.KMeans(n_clusters=nCluster)
            # 跑聚类
            clusterLabel = clusterProcessor.fit_predict(self.__npArrAfterPCA)
            # 算silhouette系数
            silAvg = silhouette_score(self.__npArrAfterPCA,clusterLabel)
            #添加到结果集
            kAndSilCur.append([nCluster, silAvg])

            silBest = silAvg if silAvg > silBest else silBest

        # 画出k和sil系数的关系函数图
        plt.plot(kAndSilCur)
        plt.savefig("k_sil.png")
        pass








if __name__ == "__main__":
    obj = Cluster()
    obj.KMCluster()
