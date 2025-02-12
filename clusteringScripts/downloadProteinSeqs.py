import urllib.request
import urllib.error
from time import time
from time import sleep
from concurrent.futures import *
import multiprocessing
import threading
import os
from glob import glob
from threading import Event

class DownloadThread(threading.Thread):
    def __init__(self, query, pathAndFileName):
        threading.Thread.__init__(self)

        self.query = query
        self.pathAndFileName = pathAndFileName
        self.didFail = False
    def run(self):
        try:
            # print("url",self.query)
            urllib.request.urlretrieve(self.query , filename=self.pathAndFileName)
        except Exception as error:
            print(self.query,"failed error caught",error)
            self.didFail = True
       




if __name__ == "__main__":
    apiKey = "541c5410ae8607fe929a6ce9ecd6ad3be309"
    loadedFiles = set(glob("/Users/cazcullimore/dev/makingPhageDataset/proteinFastas/fastas/*fasta"))
    timeToSleep = 0.3
    maxSleep = 0.3

    with open("sequence.seq") as file:
        lines = file.readlines()
        print(len(lines), len(loadedFiles))
        t1 = time()
        threads = []
        for i, line in enumerate(lines):
            id = line.strip()
            query = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi/?db=protein&id=" + id + "&retType=fasta&api_key=" + apiKey
            newFileName = "/Users/cazcullimore/dev/makingPhageDataset/proteinFastas/fastas/"+ id + ".fasta"
            # try:
            if newFileName in loadedFiles: #os.path.exists(newFileName): # 
                continue
            else:
                print(newFileName)
            # except:
            #     IDnotDownloaded = True
            # urllib.request.urlretrieve(query,filename=newFileName)
            # future = pool.submit(urllib.request.urlretrieve,(query,"/Users/cazcullimore/dev/makingPhageDataset/proteinFastas/fastas/"+ id + ".fasta"))
            donwloadDir = "/Users/cazcullimore/dev/makingPhageDataset/proteinFastas/fastas2/"+ id + ".fasta"
            thread = DownloadThread(query, donwloadDir)
            thread.start()
            threads.append(thread)
            # print("started")
            if i % 100 == 1:
                print(i/len(lines), "will take about", (len(lines) - len(loadedFiles)) / (i  - len(loadedFiles)) * (time() - t1))
            maxIters = 100000
            # while sum([1 for thread in threads if thread.is_alive()]) >= 4 and maxIters > 0:  
            #     sleep(0.001)
            #     maxIters -= 1
            for thread in threads:
                if thread.didFail and timeToSleep < maxSleep:
                    print("failed at",timeToSleep)
                    timeToSleep += 0.01
                    thread.didFail = False
            sleep(timeToSleep)
            timeToSleep *= 0.9999
            threads = threads[-10:]