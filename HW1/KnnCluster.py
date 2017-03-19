#coding: utf-8

import dataProcessor
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import numpy as np


class Knn:

    __k = [1, 2, 3, 4, 5]

    def __init__(self, mDataProcessor):

        if mDataProcessor is None:
            dP = dataProcessor.dataProcessor()
        else:
            dP = mDataProcessor

        self.__originData = dP.gridData
        self.__data = dP.dataFrame
        self.__pca = PCA()
        self.__query = [15, 250, 480, 690, 900]

    def run(self):
        array = []

        ret = {}

        for trace in self.__data:
            appendItem = self.__data.iloc[:, trace]

            array.append(appendItem)

        X = np.array(array)

        #pca降维
        pca_data = self.__pca.fit_transform(X)

        for index in self.__query:
            ret[index] = []
            for k in self.__k:
                dis, cluster = NearestNeighbors(n_neighbors=k).fit(pca_data).kneighbors(pca_data[index-1, :])

                resList = list(cluster[0, :])
                for trace in range(len(resList)):
                    resList[trace] += 1

                ret[index].append(resList)

        return ret


if __name__ == "__main__":
    test = Knn()
    test.run()





