# takes a combined fasta and makes a fasta for each group with the sequences in each group 
import sys
import os
import pickle
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


allSeqs = readInFastaAsDict(sys.argv[1])
with open("clusterGroups.p","rb") as file:
    groups = pickle.load(file)
outdirName = "msa/"

os.mkdir(outdirName)

for i, group in enumerate(groups):
    with open(os.path.join(outdirName, "group" + str(i) + ".fasta"), "w") as outfile:
        for seqName in group:
            outfile.write(">" + str(seqName) + "\n")
            outfile.write(allSeqs[str(seqName)] + "\n")

