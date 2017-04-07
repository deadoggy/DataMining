#coding: utf-8
import sklearn.cluster as cl
import pandas
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors as KNN
from sklearn.decomposition import PCA
from sklearn.metrics import  silhouette_score
from sklearn.mixture import GaussianMixture
import json

class Cluster:

    __dataFrame = pandas.DataFrame.from_csv("trace.csv")
    __npArrAfterPCA = []
    __originTraceData = []
    __initKCluster = 0
    __maxKCluster = -1
    __jsScriptName = "clusterTrace"
    __KnnK = 4
    __allLabel = {}

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
                if flag != -1:
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
        根据类变量进行聚类并画图
        返回数据结构：
        {
            k1:{
                "sil" : sil系数
                "label": [聚类结果集]
            },

            k2:{
                ...
            },
            ...
            "best" : [k, sil, [label]]
        }
    '''
    def KMCluster(self):

        kList = range(self.__initKCluster, self.__maxKCluster+1)

        silRes = []

        silBest = -1
        labelBest = []

        ret = {}

        for nCluster in kList:
            print nCluster
            # 生成一个聚类器
            clusterProcessor = cl.KMeans(n_clusters=nCluster)
            # 跑聚类
            clusterLabel = clusterProcessor.fit_predict(self.__npArrAfterPCA)
            # 算silhouette系数
            silAvg = silhouette_score(self.__npArrAfterPCA,clusterLabel)
            #添加到返回值字典中
            ret[str(nCluster)] = {"sil":silAvg, "label": clusterLabel.tolist()}
            #添加到结果集
            silRes.append(silAvg)
            if silAvg > silBest:
                labelBest = clusterLabel
                silBest = silAvg



        # 画出k和sil系数的关系函数图
        plt.plot(kList, silRes)
        plt.savefig("k_sil.png")
        #把最好的结果集添加到返回集中
        ret["best"] = [len(set(labelBest)), silBest, labelBest.tolist()]

        return ret


    '''
        DBSCAN 聚类,有两个函数
        _knnForEps() : 根据Knn找出eps的变化范围:
            假设点间距离是高斯分布， 利用极大似然估计算出均值和方差， 然后概率95%范围内为eps
        calcBestEps() : 在eps内进行DBSCAN
            先以1为步长计算拥有最好sil系数的eps值e1， 再在(e1-1, e1+1)以0.1的步长计算最好的e2，
            最后用0.01的步长计算(e2-0.01, e2+0.01)内最好的sil值 e3， ....一直到规定的精度以内，从而降低复杂度
            返回的数据结构：
                {
                    "epsrange" : [eps的范围],
                    "min_samples" : min_samples,
                    "bestEps": eps
                    "result":{
                        eps1: {
                            "sil": sil系数
                            "label": [label结果集]
                            "k": 聚类的类数量
                        },
                        eps2: {
                        ...
                        },
                        ...
                    }

                }
    '''
    def _knnForEps(self, k):

        #返回List, [low, high]
        ret = []
        #找出kNe
        kNe =KNN(n_neighbors=k).fit(self.__npArrAfterPCA)
        #Knn
        dis, cluster = kNe.kneighbors(self.__npArrAfterPCA)
        #所有的distance
        allDis = list(dis[:, k-1])

        #算方差和均值
        avgOfAllDis = np.average(allDis)
        covOfAllDis = np.cov(allDis)

        return[avgOfAllDis - 2*covOfAllDis, avgOfAllDis + 2*covOfAllDis]

    def calcBestEps(self, precision, step = 0.1, divide = 10, minSam = 2): # precision : 小数点后几位   step : 初始步长 divide : 步长的除数
        epsRange = self._knnForEps(2)
        print epsRange
        #最好值的标签
        bestSil = -1
        bestEps = 0
        #返回字典
        ret = {}
        ret["epsrange"] = epsRange
        ret["min_samples"] = minSam
        ret["bestEps"] = -1
        ret["result"] = {}
        #sil 和 k 的List, 用于画图
        silAndK = []

        for loop in range(0, precision+1): #每一级精度
            print "loop:" + str(loop)
            print "step" + str(step) + "\n"
            beg = epsRange[0]
            end = epsRange[1]


            while beg < end:
                #计算sil参数
                label = cl.DBSCAN(eps=beg, min_samples=minSam).fit_predict(self.__npArrAfterPCA)
                labelSet = set(label)
                labelSet.remove(-1)

                #如果除去噪声点后还有类
                if len(labelSet) > 0:
                    print len(labelSet)
                    print beg
                    print "**************"

                    silAvg = silhouette_score(self.__npArrAfterPCA, labels=label)
                    #添加到返回集
                    ret["result"][str(beg)] = {"sil": silAvg, "label": label.tolist(), "k": len(labelSet)}
                    #添加到画图集
                    silAndK.append([silAvg, len(labelSet)])
                    # 更新sil
                    if bestSil < silAvg:
                        bestSil = silAvg
                        bestEps = beg
                    # 步长
                beg += step

            step /= divide
            if bestEps > 0:
                epsRange = [bestEps-step, bestEps+step]

        ret["bestEps"] = bestEps

        #画图

        silAndK.sort(key = lambda x:x[1])
        X = []
        Y = []
        for item in silAndK:
            X.append(item[1])
            Y.append(item[0])
        plt.plot(X, Y)
        plt.savefig("DBSCAN_Fig_Min" + str(minSam) + ".png")
        plt.close()

        return ret


    def saveKMeansAndDBSCAN(self, label):
        resStr = json.dumps(label)
        saveFile = open("KD_res","w")
        saveFile.write(resStr)
        saveFile.close()


    '''
        把轨迹写到js脚本里
        scriptName 是文件名， 不带.js后缀,None的话用默认名字
    '''
    def writeDataToJs(self, label = None, scriptName = None):
        #获取文件名字
        name = self.__jsScriptName if scriptName is None else scriptName

        #新建文件
        traceJs = file(name + ".js", "w")

        #先写全部轨迹
        traceJs.write("var All_data=" + str(self.__originTraceData) + "\n")

        #如果有label
        if label is not None:
            traceJs.write("var labelDict = " + str(label).replace("u'", "'") + "\n")

    '''
        serilization ： True 从文件里面load出json
        高斯混合模型
        先用高斯混合模型进行聚类得出结果
        从类变量中找到KMean 和 DBSCAN 中找到最好的sil值对应的类进行比较
    '''
    def GMM(self, minSamOfDBSCAN = 2, serilization = True):

        kdLabel = {}
        if serilization:
            jsSer = open("KD_res", "r")
            kdLabel = json.load(jsSer)
        else:
            kdLabel = self.__allLabel

        #找到最好的KMeans结果
        kOfKmeans = kdLabel["KMeans"]["best"][0]
        resOfKmeans = kdLabel["KMeans"]["best"][2]

        #找到最好的DBSCAN结果
        resOfDBSCAN = []
        kOfDBSCAN = 0
        for item in kdLabel["DBSCAN"]:
            if item["min_samples"] == minSamOfDBSCAN:
                resOfDBSCAN = item["result"][str(item["bestEps"]).decode()]["label"]
                kOfDBSCAN = item["result"][str(item["bestEps"]).decode()]["k"]

        ret = {}
        for index, es in enumerate([[kOfKmeans, resOfKmeans], [kOfDBSCAN, resOfDBSCAN]]):
            GMM = GaussianMixture(n_components=es[0])
            GMM.fit(self.__npArrAfterPCA)
            label = GMM.predict(self.__npArrAfterPCA)
            print len(set(label))
            alg = "KMeans" if index == 0 else "DBSCAN"
            accur = self.calcCur([label.tolist(), es[1]])
            ret[alg] = {"k":es[0], "accuracy": accur, "label":label.tolist()}
            print accur
        return ret


    '''
        找到准确率的函数
        因为各个类的序号可能不一样，考虑到实际情况，把类中点数量最多的类的序号标记为0, 然后进行比较
    '''
    def calcCur(self, labelList):

        if len(labelList) != 2:
            return -1

        for label in labelList:
            #统计数量最多的类标号
            mostAmount = -1
            flag = 0
            for l in range(len(set(label))):
                if label.count(l) > mostAmount:
                    flag = l
                    mostAmount = label.count(l)
            #类中点数量最多的类的序号标记为0
            for index in range(0, len(label)):
                if label[index] == flag:
                    label[index] = 0
                elif label[index] == 0:
                    label[index] = flag
        return np.mean(np.array(labelList[0]).ravel() == np.array(labelList[1]).ravel())




    '''
        self.__allLabel是所有的聚类结果,数据结构如下:
        {
            "KMeans":{
                k1:{
                    "sil": sil值
                    "label" : label
                },
                ...
                "best":[K, sil]
            },
            "DBSCAN":[
                {
                    "epsrange" : [eps的范围],
                    "min_samples" : min_samples,
                    "bestEps": eps
                    "result":{
                        eps1: {
                            "sil": sil系数
                            "label": [label结果集]
                            "k": 聚类的类数量
                        },
                        eps2: {
                        ...
                        },
                        ...
                    }
                },
                {
                    ... //min_sample 不同
                }
            ],

            "GMM":{
                "KMeans":{
                    "k" : K,
                    "accuracy" : accruacy,
                    "label" : [label]
                },

                "DBSCAN":{
                    "k" : K,
                    "accuracy" : accruacy,
                    "label" : [label]
                }
            }

        }
    '''
    def mainLogic(self):

        # # DBSCAN
        # print "DBSCAN"
        # self.__allLabel["DBSCAN"] = []
        # for i in range(2, 5):
        #     self.__allLabel["DBSCAN"].append(self.calcBestEps(precision=4, minSam=i))
        #
        # KMeans
        # print "KMeans"
        # self.__allLabel["KMeans"] = self.KMCluster()
        #
        # #持久化
        # self.saveKMeansAndDBSCAN(self.__allLabel)

        self.__allLabel = json.load(open("KD_res", "r"))

        #GMM
        self.__allLabel["GMM"] = self.GMM()

        print "Writing"
        self.writeDataToJs(label=self.__allLabel)
        print "Done"




if __name__ == "__main__":

    obj = Cluster(initK=2, maxK=100)
    obj.mainLogic()





