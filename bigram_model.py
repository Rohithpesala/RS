import pandas as pd
import csv
from collections import defaultdict
import numpy as np
from datetime import datetime
from sets import Set
import math

#----------------------------------------------------------------------------------------------------------------------------------------
#Part 1 - Loading train and test data for eval
#lists of user item pairs
traind = defaultdict(list)
testd = defaultdict(Set)
file_path_test = 'Processed_data_test.csv'
testfile = open(file_path_test, 'rb')
testset = csv.reader(testfile, delimiter=',')
file_path_train = 'Processed_data_train.csv'
trainfile = open(file_path_train,'rb')
trainset = csv.reader(trainfile, delimiter = ',')
for row in trainset:
    traind[str(row[0])].append(str(row[1]))
for row in testset:
    testd[str(row[0])].add(str(row[1]))


#----------------------------------------------------------------------------------------------------------------------------------------
#Part 2 - Read the train file and generate bigram counts
i=1
p=1
prev= ''
dfile = open(file_path_train, 'rb')
dreader = csv.reader(dfile, delimiter=',')
ud = defaultdict(int) #Contains the bigrams merged with || and later processed. This is to get the count of bigrams
c = 0
for row in dreader:
    if i == 1:    	#Base case - Avoid including header to data
        i+=1
        continue
    if i-p==1:		#First item for a given user
        prev = str(row[1])
        c+=1#print prev
    else:
        s = prev+"||"+str(row[1])
        prev = str(row[1])
        ud[s]+=1    
    if i-p ==dd[row[0]]:	#Last item for a given user
        #only testing purposes
        #s = prev+"||end"
        #ud[s]+=1 
        #print "haa",i,p,d[k["User id"]]
        p = i
    i+=1
    #if t>100:break

#----------------------------------------------------------------------------------------------------------------------------------------
#Part 3 - Process those bigrams into a list of list of tuple and sort them
ud_proccessed = defaultdict(list) #We now process them to get a sorted list out with the counts
c = 0
for k in ud.keys():
    #print k
    i,j = k.split("||")
    ud_proccessed[i].append((j,ud[k]))
for k in ud_proccessed.keys():
    ud_proccessed[k].sort(key=lambda x: x[1],reverse=True)
    if len(ud_proccessed[k])>1:
        c+=len(ud_proccessed[k])

#Load item data
ilist = [ i for i in ud_proccessed.keys() ]

#----------------------------------------------------------------------------------------------------------------------------------------
#Part 4 - Produce a list of 10 items to calc perf
st = datetime.now()
prec10 = 0
prec2 = 0
recall10 = 0
recall2 = 0
fm10 = 0
fm2 = 0
c=0
for k in traind.keys():
    c+=1
    #if c!=13244:
    #    continue
    if c%1000==0:
        print c/1000, datetime.now()-st
    recoset = Set()
    recolist = []
    s = traind[k][len(traind[k])-1]
    ps = ""
    #print s,k
    n = 0
    l = 0
    while(l<10):
        #This occurs when the item doesn't have any successors. So, we randomly assign a item but below we see that we first explore through our list
        while s not in ilist or ps == s:
            rn = int(math.floor(np.random.random()*len(ilist))) #Getting the random index
            s = str(ilist[rn]) 
        ps = s
        #print c,s, s in ud_proccessed.keys()
        pl = ud_proccessed[s]
        for i in range(len(pl)):
            if l>=10:
                break
            if pl[i][0] not in recoset:
                recoset.add(pl[i][0])
                recolist.append(pl[i][0])
                l+=1
        while(1):
            if n<l:
                s = recolist[n]
                n+=1
                #print n,
                if s in ilist:
                    break
            else:
                break
    intlist10 = Set(recolist) & testd[k]
    intlist2  = Set(recolist[0:2]) & testd[k]
    prec10 += len(intlist10)/10.0
    prec2 += len(intlist2)/2.0
    recall10 += len(intlist10)*1.0/len(testd[k])
    recall2 += len(intlist2)*1.0/len(testd[k])
    #break

prec10 /= len(traind)
prec2 /= len(traind)
recall10 /= len(traind)
recall2 /= len(traind)     
fm10 = 2*prec10*recall10/(prec10+recall10)
fm2 = 2*prec2*recall2/(prec2+recall2)
print c    
print datetime.now()-st

print prec2,recall2,fm2,prec10,recall10,fm10