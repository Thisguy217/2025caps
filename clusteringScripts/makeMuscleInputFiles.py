# takes a combined fasta and makes a fasta for each group with the sequences in each group 
from blastGroups import * # these groups have to be updated it is just a python file with a list of sets that contains the names of each sequence in the group
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


allSeqs = readInFastaAsDict(sys.argv[1])

for i, group in enumerate(groups):
    with open("blastGroupMsa/group" + str(i) + ".fasta", "w") as outfile:
        for seqName in group:
            outfile.write(">" + str(seqName) + "\n")
            outfile.write(allSeqs[str(seqName)] + "\n")

