#coding: utf-8

from dataProcessor import  *
from Hash import *
from KnnCluster import *
from dataProcessor import *


if __name__ == "__main__":

    dp = dataProcessor()

    hashObj = HashData(dp)
    knnObj = Knn(dp)

    hashRes = hashObj.run()
    knnRes = knnObj.run()

    dp.drawTrace()


    for query_trace in knnRes:
         group = knnRes[query_trace]
         for k, k_res in enumerate(group):
             dp.drawTrace(k_res,"knn_query%d_k%d"%(query_trace, k+1))

    for hashSize in hashRes:
        traceToQueryList = hashRes[hashSize]
        for traceToQuery in traceToQueryList:
            resGroup = traceToQuery[1]
            tid = []
            for resTrace in resGroup:
                tid.append(resTrace[0][1].tid)

            dp.drawTrace(tid, "lsh_query%d_size%d"%(traceToQuery[0], hashSize))

