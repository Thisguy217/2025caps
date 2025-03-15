

from glob import glob
import re
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


def getMode(seqs):
    seqs = list(seqs)
    seqLengths = np.array([len(seq) for seq in seqs])
    x_d = np.linspace(min(seqLengths),max(seqLengths), 1000)
    density = sum(norm(xi,scale=10).pdf(x_d) for xi in seqLengths)
    """ plotting and multiple modes
    plt.fill_between(x_d, density, alpha=0.5)
    plt.plot(x, np.full_like(x, -0.1), '|k', markeredgewidth=1)
    plt.show()

    for i in range(len(density) - 1):
        if density[i] > density[i+1] and density[i] > density[i-1]:
            print("max at",x_d[i]) """
    densityMode = x_d[np.argmax(np.array(density))]
    return densityMode

def getSeqOfModeLength(seqs):
    densityMode = getMode(seqs)
    seqLengths = np.array([len(seq) for seq in seqs])
    dists = np.array([(seqLength - densityMode)**2 for seqLength in seqLengths])
    indexOfClosestSeq = np.argmin(dists)
    closestSeq = seqs[indexOfClosestSeq]
    # print("seq len",len(closestSeq))
    return closestSeq

def getConservedIndexes(fileName, seqToMatch=None,getMode=False):

    file = readInFastaAsDict(fileName)
    msaLength = len(list(file.values())[0])
    unalignedSeqs = [seq.replace("-","") for seq in file.values()]
    if getMode:
        seqToMatch = getSeqOfModeLength(unalignedSeqs)
    seqIndexToMatch = unalignedSeqs.index(seqToMatch)

   

    conservedIndexes = []
    numDashes = 0
    for i in range(msaLength):
        aa = ""
        isConserved=True
        for seqIndex, seq in enumerate(file.values()):
            if aa == "":
                aa = seq[i]
            else:
                if aa != seq[i]:
                    isConserved=False
#                print(seqIndex,seq[i])
            if seqIndex == seqIndexToMatch and seq[i] == "-":
                numDashes += 1
        if isConserved:
            conservedIndexes.append(i - numDashes+1)
        

    return fileName, len(list(file.keys())),len(conservedIndexes),msaLength, conservedIndexes, seqToMatch

if __name__ == "__main__":
    import numpy as np
    from scipy.stats import norm
    if len(sys.argv) == 1:
        print("please give a list of the msa files for each group")
    print("groupName\tnumSeqs\tnumConserved\tMSAlength\tConservedIndices\trepresentativeSequence")
    for fileName in sys.argv[1:]:
        output = getConservedIndexes(fileName)
        print(*output,sep="\t")
        

        
