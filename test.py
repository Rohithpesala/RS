import csv
import pandas as pd
t = 0

csvpathr = "ratings_Clothing_Shoes_and_Jewelry.csv"
csvpathw = "Data_" + csvpathr
df = pd.read_csv(csvpathr)
#df = df.sort(["User id", "Timestamp"])
print df[0:20]


'''
with open(csvpathw, 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')	
	spamwriter.writerow(['User id', 'Item id', 'Rating','Timestamp'])
	with open(csvpathr, 'rb') as cfile:
		reader = csv.reader(cfile, delimiter=',')
		spamwriter.writerows(row for row in reader)

		for row in reader:
			spamwriter.writerow

'''
'''
with open('ratings_Clothing_Shoes_and_Jewelry.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		row[1], row[3] = row[3], row[1]
		print '||'.join(row), "||", len(row[0])
		t += 1
		if t>20: break
'''