import pandas as pd
import csv
from surprise import BaselineOnly,NormalPredictor,SVD,NMF,KNNBasic,KNNBaseline,Reader,Dataset
import numpy as np

#Defining performance measures
def rmse(pred):    
    mse = np.mean([float((real - est)**2) for real,est in pred])
    rmse_ = np.sqrt(mse)
    return rmse_
def mae(pred):
    mae_ = np.mean([float(abs(real - est)) for real,est in pred])
    return mae_


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

#Training with algo
algo1 = NMF()
algo1.train(trainset)

#predictions
preds1 = []
for row in testset:
    #print row
    pred = algo1.predict(str(row[0]), str(row[1]), r_ui=float(row[2]))
    preds1.append((pred[2],pred[3]))
    #break
#print preds


#Performance measures
rmse1 = rmse(preds1)
mae1 = mae(preds1)
print rmse1,mae1
testfile.close()