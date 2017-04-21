import csv
import pandas as pd
from sets import Set

filepath = "Processed_data.csv"
dfile = open(filepath,'rb')
df= pd.read_csv(dfile)
itemfile = "items.txt"
ifile = open(itemfile,'w')
userfile = "users.txt"
ufile = open(userfile,'w')

iset = Set(df['Item id'])
uset = Set(df['User id'])

print len(iset)
c = 0
for x in iset:
    c+=1
    ifile.write(str(x))
    if c!=len(iset):
        ifile.write('\n')
ifile.close()

print len(uset)
c = 0
for x in uset:
    c+=1
    ufile.write(str(x))
    if c!=len(uset):
        ufile.write('\n')
ufile.close()
