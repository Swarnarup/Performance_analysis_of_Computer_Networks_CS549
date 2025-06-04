import os
import datetime
import pandas as pd

files = {'1kb':1, '10kb':10, '100kb':100, '1mb':1024, '10mb':1024*10, '100mb':1024*100}
methods = ['fgetc', 'fread']

fgetcList = []
freadList = []

for m in methods:
    totalTime = 0
    if(m == 'fgetc'):
        for file in files:
            downloadStart = datetime.datetime.now()
            os.system(f"./fgetc.out {file}.txt")
            downloadEnd = datetime.datetime.now()
            totalTime = downloadEnd - downloadStart
            fgetcList.append(files[file]/totalTime.total_seconds())
            
            
    else:
        for file in files:
            downloadStart = datetime.datetime.now()
            os.system(f"./fread.out {file}.txt")
            downloadEnd = datetime.datetime.now()
            totalTime = downloadEnd - downloadStart
            freadList.append(files[file]/totalTime.total_seconds())
            
    


df = pd.DataFrame({'fgetc': fgetcList, 'fread':freadList}, index = list(files.keys()))
df.index.name = "file size"
print(df)
df.to_csv("data3.csv")
