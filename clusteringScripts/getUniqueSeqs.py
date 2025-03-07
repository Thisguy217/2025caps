import sys
import re

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

uniqueSeqs = {}
inFileName = sys.argv[1]
removedDuplicateFileName = re.sub(r"(\..*)$", r"RemovedDuplicates\1",inFileName)
for name, seq in readInFastaAsDict(inFileName).items():
    if not seq in uniqueSeqs.values():
        uniqueSeqs[name] = seq

print(len(list(uniqueSeqs.keys())))

with open(removedDuplicateFileName, "w") as outfile:
    for name, seq in uniqueSeqs.items():
        outfile.write(">" + name + "\n" + seq + "\n")
