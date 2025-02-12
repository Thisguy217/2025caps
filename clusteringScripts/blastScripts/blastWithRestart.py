import os
import random
import re
import subprocess
from multiprocessing import Pool
from glob import glob
from concurrent.futures import *
import pandas as pd
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

def runBlast(queryFile,subjectFile,outFile):
    with open(outFile,"a") as out:
        subprocess.run(("blastp -query " + queryFile + " -subject " + subjectFile + " -outfmt 6").split(), stdout=out)


def getQueryNames(blastOutputFileName):
    """looks like this: 
        129	128189	93.443	122	8	0	1	122	1	122	1.06e-84	244
    """
    
    blastOutput = pd.read_csv(blastOutputFileName, sep="\t")
    print(blastOutput)
    queryNames = blastOutput["query acc.ver"].tolist()
    if len(queryNames) == 0:
        return set()
    # redo last protein in case of incomplete blast
    lastElt = queryNames[-1]
    while len(queryNames) > 0 and queryNames[-1] == lastElt:
        queryNames.pop()
    queryNames = set(queryNames)
    return queryNames

def runNextAssignedBlast(assignedQueryFileName,subjectFileName,blastOutputFileName): # each job has its own list of assigned queries
    
    
    assignedQueries = readInFastaAsDict(assignedQueryFileName) 
    
    

    queriesRan = getQueryNames(blastOutputFileName) # do we want to name queries?
    queryNamesToRun = set(assignedQueries.keys()).difference(queriesRan)
    queriesToRunFileName = "temp_queriesToRun.fasta"
    with open(queriesToRunFileName, "w") as queriesToRunFile: 
        for name in queryNamesToRun:
            queriesToRunFile.write(">" + name + "\n")
            queriesToRunFile.write(assignedQueries[name] + "\n")

    runBlast(queriesToRunFileName, subjectFileName,blastOutputFileName)
    os.remove(queriesToRunFileName)

if __name__ == "__main__":

    assignedQueryFileName = sys.argv[1]
    subjectFileName = sys.argv[2]
    try:
        blastOutputFileName = sys.argv[3]
    except IndexError:
        blastOutputFileName = "blastOut.tsv"

    header = "query acc.ver\tsubject acc.ver\t% identity\talignment length\tmismatches\tgap opens\tq. start\tq. end\ts. start\ts. end\tevalue\tbit score\n"
    if not os.path.exists(blastOutputFileName):
        with open(blastOutputFileName, "w") as out:
            out.write(header)
    runNextAssignedBlast(assignedQueryFileName,subjectFileName,blastOutputFileName)