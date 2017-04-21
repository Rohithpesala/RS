import pandas as pd
import csv
from surprise import BaselineOnly,NormalPredictor,SVD,SVDpp,NMF,KNNBasic,KNNBaseline,Reader,Dataset,CoClustering
import numpy as np
from collections import defaultdict
from datetime import datetime
from sets import Set
import math

#Loading data
#train data
file_path_train = 'Processed_data_train.csv'
reader = Reader(line_format='user item rating timestamp', sep=',')
trainset = Dataset.load_from_file(file_path_train, reader=reader)
trainset = trainset.build_full_trainset()

#test data
file_path_test = 'Processed_data_test.csv'
testfile = open(file_path_test, 'rb')
testset = csv.reader(testfile, delimiter=',')

#Load item data
itemfile = "items.txt"
ifile = open(itemfile,'r')
ilist = [ i for i in ifile.readlines() ]

#Training with algo
algo1 = NormalPredictor()
algo1.train(trainset)
algo2 = BaselineOnly()
algo2.train(trainset)
algo3 = NMF(n_factors=100,n_epochs=50)
algo3.train(trainset)
algo4 = SVD(n_factors=100,n_epochs=50)
algo4.train(trainset)

#lists of user item pairs
traind = defaultdict(Set)
testd = defaultdict(Set)
tfile = open(file_path_train,'rb')
tset = csv.reader(tfile, delimiter = ',')
for row in tset:
    traind[str(row[0])].add(str(row[1]))
for row in testset:
    testd[str(row[0])].add(str(row[1]))
print len(traind),len(testd)    


#predictions
#iterating through all users
startTime = datetime.now()

precision2_1 = 0
recall2_1 = 0
precision10_1 = 0
recall10_1 = 0

precision2_2 = 0
recall2_2 = 0
precision10_2 = 0
recall10_2 = 0

precision2_3 = 0
recall2_3 = 0
precision10_3 = 0
recall10_3 = 0

precision2_4 = 0
recall2_4 = 0
precision10_4 = 0
recall10_4 = 0

c=0
for k in traind.keys():
    c+=1
    if c%10000==0:
        print c/10000, datetime.now() - startTime
        #break
    recoset = Set() #Using a set to track the items we got a rating for
    recolist1 = []   #Using a lis to track the items and the rating and later sort to get top n recos
    recolist2 = []   #Using a lis to track the items and the rating and later sort to get top n recos
    recolist3 = []   #Using a lis to track the items and the rating and later sort to get top n recos
    recolist4 = []   #Using a lis to track the items and the rating and later sort to get top n recos
    for x in testd[k]: # Iterating through all test items of the particular user and add them to our set
        recoset.add(x)
        #Predicting the ratings for all the items in test set w.r.t all our algorithms
        pred1 = algo1.predict(k, x, r_ui=3.0)
        recolist1.append((x,pred1[3]))
        pred2 = algo2.predict(k, x, r_ui=3.0)
        recolist2.append((x,pred2[3]))
        pred3 = algo3.predict(k, x, r_ui=3.0)
        recolist3.append((x,pred3[3]))
        pred4 = algo4.predict(k, x, r_ui=3.0)
        recolist4.append((x,pred4[3]))
        
    for i in range(1000): # Adding 1000 random items to simulate the unknown environment
        rn = int(math.floor(np.random.random()*len(ilist))) #Getting the random index
        ritem = str(ilist[rn])
        while(ritem in traind[k] or ritem in recoset):
            rn = int(math.floor(np.random.random()*len(ilist))) #Getting the random index
            ritem = str(ilist[rn])
        recoset.add(ritem)
        pred1 = algo1.predict(k, ritem, r_ui=3.0)        
        recolist1.append((ritem,pred1[3]))
        pred2 = algo2.predict(k, ritem, r_ui=3.0)        
        recolist2.append((ritem,pred2[3]))
        pred3 = algo3.predict(k, ritem, r_ui=3.0)
        recolist3.append((ritem,pred3[3]))
        pred4 = algo4.predict(k, ritem, r_ui=3.0)
        recolist4.append((ritem,pred4[3]))
    #Sorting the recolists to extract top N recos
    recolist1.sort(key=lambda x: x[1],reverse=True)
    toplist1 = []
    recolist2.sort(key=lambda x: x[1],reverse=True)
    toplist2 = []
    recolist3.sort(key=lambda x: x[1],reverse=True)
    toplist3 = []
    recolist4.sort(key=lambda x: x[1],reverse=True)
    toplist4 = []
    for i in range(10):
        toplist1.append(recolist1[i][0])    
        toplist2.append(recolist2[i][0])
        toplist3.append(recolist3[i][0])    
        toplist4.append(recolist4[i][0])
    intlist10_1 = Set(toplist1) & testd[k]
    intlist2_1 = Set(toplist1[0:2]) & testd[k]
    intlist10_2 = Set(toplist2) & testd[k]
    intlist2_2 = Set(toplist2[0:2]) & testd[k]
    intlist10_3 = Set(toplist3) & testd[k]
    intlist2_3 = Set(toplist3[0:2]) & testd[k]
    intlist10_4 = Set(toplist4) & testd[k]
    intlist2_4 = Set(toplist4[0:2]) & testd[k]
    #Precision
    precision10_1 += len(intlist10_1)*1.0/10
    precision2_1 += len(intlist2_1)*1.0/2
    precision10_2 += len(intlist10_2)*1.0/10
    precision2_2 += len(intlist2_2)*1.0/2
    precision10_3 += len(intlist10_3)*1.0/10
    precision2_3 += len(intlist2_3)*1.0/2
    precision10_4 += len(intlist10_4)*1.0/10
    precision2_4 += len(intlist2_4)*1.0/2
    #Recall
    recall10_1 += len(intlist10_1)*1.0/len(testd[k])
    recall2_1 += len(intlist2_1)*1.0/len(testd[k])
    recall10_2 += len(intlist10_2)*1.0/len(testd[k])
    recall2_2 += len(intlist2_2)*1.0/len(testd[k])
    recall10_3 += len(intlist10_3)*1.0/len(testd[k])
    recall2_3 += len(intlist2_3)*1.0/len(testd[k])
    recall10_4 += len(intlist10_4)*1.0/len(testd[k])
    recall2_4 += len(intlist2_4)*1.0/len(testd[k])
    #break
precision10_1 /=len(traind)
precision2_1 /=len(traind)
precision10_2 /=len(traind)
precision2_2 /=len(traind)
precision10_3 /=len(traind)
precision2_3 /=len(traind)
precision10_4 /=len(traind)
precision2_4 /=len(traind)

recall10_1 /=len(traind)
recall2_1 /=len(traind)
recall10_2 /=len(traind)
recall2_2 /=len(traind)
recall10_3 /=len(traind)
recall2_3 /=len(traind)
recall10_4 /=len(traind)
recall2_4 /=len(traind)

fm10_1 = 2*precision10_1*recall10_1/(precision10_1 + recall10_1)
fm2_1 = 2*precision2_1*recall2_1/(precision2_1 + recall2_1)
fm10_2 = 2*precision10_2*recall10_2/(precision10_2 + recall10_2)
fm2_2 = 2*precision2_2*recall2_2/(precision2_2 + recall2_2)
fm10_3 = 2*precision10_3*recall10_3/(precision10_3 + recall10_3)
fm2_3 = 2*precision2_3*recall2_3/(precision2_3 + recall2_3)
fm10_4 = 2*precision10_4*recall10_4/(precision10_4 + recall10_4)
fm2_4 = 2*precision2_4*recall2_4/(precision2_4 + recall2_4)
print datetime.now() - startTime

#Printing performance measures
print precision2_1, recall2_1, fm2_1, precision10_1, recall10_1,fm10_1
print precision2_2, recall2_2, fm2_2, precision10_2, recall10_2,fm10_2
print precision2_3, recall2_3, fm2_3, precision10_3, recall10_3,fm10_3
print precision2_4, recall2_4, fm2_4, precision10_4, recall10_4,fm10_4
