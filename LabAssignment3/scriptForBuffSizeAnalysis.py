import os
import datetime
import pandas as pd

files = {'1kb':1, '10kb':10, '100kb':100, '1mb':1024, '10mb':1024*10, '100mb':1024*100}
buffSizes = [1, 10, 100, 1000, 10000, 100000]

d = {}
for bs in buffSizes:
    dd = {}
    for file in files:
        downloadStart = datetime.datetime.now()
        os.system(f"./fread_with_buffSize.out {file}.txt {bs}")
        downloadEnd = datetime.datetime.now()
        totalTime = downloadEnd - downloadStart

        dd[file]= (files[file]/totalTime.total_seconds())
    d["buffSize="+str(bs)] = dd
            
 


# df = pd.DataFrame({'buffSize' : arr}, index = list(files.keys()))
df = pd.DataFrame.from_dict(d)
df.index.name = "file size"
print(df)
df.to_csv("dataForBuffSizeVariation.csv")