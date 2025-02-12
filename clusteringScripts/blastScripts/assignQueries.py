import os
import sys
def assignQueries(allSeqsFastaName, numWorkers):

    dividedQueryFiles = []
    for i in range(numWorkers):
        dir = "blastJob" + str(i)
        if not os.path.exists(dir):
            os.mkdir(dir)
        dividedQueryFiles.append(open(os.path.join(dir, "queries.fasta"), "w"))
    
    i = 0
    title = "no title"
    with open(allSeqsFastaName) as seqFile:
        for line in seqFile: # assumes one line fasta
        
            if len(line) == 0:
                raise Exception("empty line on fasta")
            if line[0] != ">":
                dividedQueryFiles[i % len(dividedQueryFiles)].write(title + line)
                i += 1
            else:
                title = line
            
    for file in dividedQueryFiles:
        file.close()

if __name__ == "__main__":
    assignQueries(sys.argv[1], int(sys.argv[2]))