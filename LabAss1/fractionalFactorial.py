import os
import threading
import datetime
import csv

strToInt = {"1B": 1,
        "1kB": 1024,
        "10kB": 10240,
        "100kB": 102400,
        "500kB": 1024*500,
        "1MB": 1024*1024,
        "10MB": 1024*1024*10,
        "100MB": 1024*1024*100,
        "500MB": 1024*1024*500
    }

def mainDownload(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer):
    downloadStart = datetime.datetime.now()
    os.system('wget -P down --limit-rate '+downloadSpeedLimit+' '+lst[fileSize])
    downloadEnd = datetime.datetime.now()
    totalTime = downloadEnd - downloadStart

    writer.writerow([fileSize, downloadSpeedLimit, noOfConJobs, strToInt[fileSize]/totalTime.total_seconds(), totalTime.total_seconds()])

def concurrentDownload(lst, fileSize, downloadSpeedLimit):
    os.system('wget -P down --limit-rate '+downloadSpeedLimit+' '+lst[fileSize])

def downloadFiles(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer):
    threadLst = []
    for i in range(noOfConJobs-1):
        t = threading.Thread(target=concurrentDownload, args=(lst, fileSize, downloadSpeedLimit))
        threadLst.append(t)
    
    t = threading.Thread(target=mainDownload, args=(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer))
    threadLst.append(t)

    for t in threadLst:
        t.start()
    for t in threadLst:
        t.join()

    print("Done!")
 

if __name__ =="__main__":

    # taking highest and lowest download size
    links = {"1B": "https://cloud.iitmandi.ac.in/f/104e18c7689843d38646/?dl=1",
            "500MB": "https://cloud.iitmandi.ac.in/f/bf9f34fc8eec43ee991e/?dl=1"
        }
    
    # taking highest and lowest download speed limit
    downLooadSpeedLimit = ["500k", "inf"]

    # taking highest and lowest no of concurrent downloads
    noOfConDownloads = [1, 7]

    file = open("fractional_design_highest_and_lowest_4PM.csv", mode='a', newline='')
    writer = csv.writer(file)
    writer.writerow(["File Size", "Download Speed Limit", "No. of Concurrent Downloads", "Throughput (bite/seconds)", "Delay (seconds)"])

    for sz in  links:
        for lims in downLooadSpeedLimit:
            for nProcs in noOfConDownloads:
                print(f'starting {sz} {lims} {nProcs}')
                downloadFiles(links, sz, lims, nProcs, writer)
                print(f'ending {sz} {lims} {nProcs}')
    
    file.close()

