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

def mainDownload(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer, temp):
    downloadStart = datetime.datetime.now()
    os.system('wget -P down --limit-rate '+downloadSpeedLimit+' '+lst[fileSize])
    downloadEnd = datetime.datetime.now()
    totalTime = downloadEnd - downloadStart

    temp[0] = strToInt[fileSize]/totalTime.total_seconds()
    writer.writerow([fileSize, downloadSpeedLimit, noOfConJobs, strToInt[fileSize]/totalTime.total_seconds(), totalTime.total_seconds()])

def concurrentDownload(lst, fileSize, downloadSpeedLimit):
    os.system('wget -P down --limit-rate '+downloadSpeedLimit+' '+lst[fileSize])

def downloadFiles(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer, temp):
    threadLst = []
    for i in range(noOfConJobs-1):
        t = threading.Thread(target=concurrentDownload, args=(lst, fileSize, downloadSpeedLimit))
        threadLst.append(t)
    
    t = threading.Thread(target=mainDownload, args=(lst, fileSize, downloadSpeedLimit, noOfConJobs, writer, temp))
    threadLst.append(t)

    for t in threadLst:
        t.start()
    for t in threadLst:
        t.join()

    print("Done!")
 

if __name__ =="__main__":

    links = {"1B": "https://cloud.iitmandi.ac.in/f/104e18c7689843d38646/?dl=1",
            "1kB": "https://cloud.iitmandi.ac.in/f/34f236050c354ac995dc/?dl=1",
            "10kB": "https://cloud.iitmandi.ac.in/f/f2136456bcf6439eaf18/?dl=1",
            "100kB": "https://cloud.iitmandi.ac.in/f/c3b76d27af45462db019/?dl=1",
            "500kB": "https://cloud.iitmandi.ac.in/f/3c2970f86ea8449c84d1/?dl=1",
            "1MB": "https://cloud.iitmandi.ac.in/f/dcd4883d914a44fb9850/?dl=1",
            "10MB": "https://cloud.iitmandi.ac.in/f/390c9e71032d4f30a6ca/?dl=1",
            "100MB": "https://cloud.iitmandi.ac.in/f/4b2c32ec021e4de4a710/?dl=1",
            "500MB": "https://cloud.iitmandi.ac.in/f/bf9f34fc8eec43ee991e/?dl=1"
        }
    


    downloadSpeedLimit = ["500k", "1M", "1.5M", "2M", "inf"]
    noOfConDownloads = [1, 3, 5, 7]
    timeOfDay = ["12AM", "8PM"]

    file = open("simple_Design_4PM.csv", mode='a', newline='')
    writer = csv.writer(file)
    writer.writerow(["File Size", "Download Speed Limit", "No. of Concurrent Downloads", "Throughput (bite/seconds)", "Delay (seconds)"])

    # most influential factor in download speed limit 
    dsl = "inf"
    fileSz = "10kB"
    nocd = 3
    
    maxTp = float('-inf')
    for i in range(len(downloadSpeedLimit)):
        tmp = [0]
        downloadFiles(links, fileSz, downloadSpeedLimit[i], nocd, writer, tmp)
        if(tmp[0] > maxTp):
            maxTp = tmp[0]
            dsl = downloadSpeedLimit[i]

    maxTp = float('-inf')
    for i in range(len(noOfConDownloads)):
        tmp = [0]
        downloadFiles(links, fileSz, dsl, noOfConDownloads[i], writer, tmp)
        if(tmp[0] > maxTp):
            maxTp = tmp[0]
            nocd = noOfConDownloads[i]

    maxTp = float('-inf')
    for sz in links:
        tmp = [0]
        downloadFiles(links, sz, dsl, nocd, writer, tmp)
        if(tmp[0] > maxTp):
            maxTp = tmp[0]
            fileSz = sz
    
    print("Most throughput is at filesize: "+fileSz+", download Speed Limit: "+dsl+", no. of concurrent downloads: "+str(nocd))
    print("Maximum throughput is : "+str(maxTp))
    file.close()

