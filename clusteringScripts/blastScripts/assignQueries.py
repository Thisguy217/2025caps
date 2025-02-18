import os
import sys


def readInFastaAsDict(fileName):
    fileData = {}
    with open(fileName) as file:
        entryData = []
        lastGenomeName = ""
        for line in file:
            if line[0] == ">":
                if entryData != []:
                    fileData[lastGenomeName] = ''.join(entryData)
                lastGenomeName = line[1:].strip()
                entryData = []
            else:
               entryData.append(line.strip())
        fileData[lastGenomeName] = ''.join(entryData)
    return fileData

def assignQueries(allSeqsFastaName, numWorkers):

    dividedQueryFiles = []
    for i in range(numWorkers):
        dir = "blastJob" + str(i)
        if not os.path.exists(dir):
            os.mkdir(dir)
        dividedQueryFiles.append(open(os.path.join(dir, "queries.fasta"), "w"))
    
    i = 0
    allSeqsFasta = readInFastaAsDict(allSeqsFastaName)
    for proteinName, proteinSeq in allSeqsFasta.items(): # assumes one line fasta
        dividedQueryFiles[i % len(dividedQueryFiles)].write(">" + proteinName + "\n" + proteinSeq + "\n")
        i += 1
            
    for file in dividedQueryFiles:
        file.close()

if __name__ == "__main__":
    assignQueries(sys.argv[1], int(sys.argv[2]))
