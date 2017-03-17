#coding: utf-8

from dataProcessor import dataProcessor as dP
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

class Knn:

    def __init__(self):

        dataProcessor = dP()
        self.__originData = dataProcessor.readFile()
        self.__data = dataProcessor.tansferDataToGridMatrix(self.__originData)
        self.__pca = PCA()

    def run(self):
        array = []

        for trace in self.__data:
            appendItem = self.__data.iloc[:, trace]
            array.append(appendItem)

        X = np.array(array)

        #pca降维
        pca_data = self.__pca.fit_transform(X)

        dis,cluster = NearestNeighbors().fit(X).kneighbors(X)

        print "未降维：\n"
        for group in cluster:
            print group

        dis,cluster = NearestNeighbors().fit(pca_data).kneighbors(pca_data)

        print "pca降维：\n"
        for group in cluster:
            print group

if __name__ == "__main__":
    test = Knn()
    test.run()





