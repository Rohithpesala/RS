import csv
import pandas as pd
import math

t = 0

csvpathr = "ratings_Clothing_Shoes_and_Jewelry.csv"   	#Reading the raw data in csv format
csvpathw = "Data_" + csvpathr							#Writinng with header

#Writing the Header row to avoid data loss and easy loading to dataframes
with open(csvpathw, 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')	
	spamwriter.writerow(['User id', 'Item id', 'Rating','Timestamp'])	#The header
	with open(csvpathr, 'rb') as cfile:
		reader = csv.reader(cfile, delimiter=',')
		spamwriter.writerows(row for row in reader)

#Sorting the data w.r.t UID (Stratified split) and Timestamp(Temporal)
df = pd.read_csv(csvpathw)
df = df.sort(["User id", "Timestamp"])
#print df[0:20]

#Writing the processed data out to a file (Discarding all users who bought less than 5 items)
outpath = "Processed_data.csv"
outf = open(outpath,'w')
cw = csv.writer(outf, delimiter=',')
cw.writerow(['User id', 'Item id', 'Rating','Timestamp'])
t=0
for i,k in df.iterrows():
    if d[k["User id"]] >=5:
        t+=1
        cw.writerow(k)
        #if t>100: break
outf.close()

#Splitting the processed data into train and test sets
t=0
ndf = pd.read_csv(outpath)
trainpath = "Processed_data_train.csv"
trainf = open(trainpath,'w')
trw = csv.writer(trainf, delimiter=',')
testpath = "Processed_data_test.csv"
testf = open(testpath,'w')
tew = csv.writer(testf, delimiter=',')
p=-1
for i,k in ndf.iterrows():
    t+=1
    
    lim = int(math.ceil(0.8*d[k["User id"]]))	#split param
    #print i,p,d[k["User id"]],lim
    if i-p <=lim:
        trw.writerow(k)        
    else:
        tew.writerow(k)
    if i-p ==d[k["User id"]]:
        #print "haa",i,p,d[k["User id"]]
        p = i
    #if t>100:break
trainf.close()
testf.close()