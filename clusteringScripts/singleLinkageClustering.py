# makes groups to be used for a muscle MSA based on a single linkage
import pandas as pd
from copy import deepcopy
import sys

EVALUE_INDEX = -2
QUERY_NAME_INDEX = 0
SUBJECT_NAME_INDX = 1



if __name__ == "__main__":

    blastOutputFileName = sys.argv[1]#"blastOut.tsv"
    print(blastOutputFileName,"blastArg")
    blastOutput = pd.read_csv(blastOutputFileName, sep="\t")
    print("read file")
    print(blastOutput.columns)
    print(blastOutput)
    queryNames = set(blastOutput["query acc.ver"].tolist())
    
    # familes = [set(name) for name in queryNames]

    similarProteins = []
    blastOutput = blastOutput.loc[blastOutput["evalue"] < 1e-10]
    for name in queryNames:
        famForThisProtein = set(blastOutput.loc[blastOutput["query acc.ver"] == name]["subject acc.ver"].tolist())
        similarProteins.append(famForThisProtein)

    print(similarProteins)
    with open("clusters", "w") as out:

        print("groups =",similarProteins,file=out)
    exit(0)
    # now we have a set of proteins and we need to merge sets that have overlapping proteins


    # while True:
    #     print(len(similarProteins))
    #     lastSimProteins = []
    #     changed = False
    #     for i,fam1 in enumerate(similarProteins):
    #         # foundMatch = False
    #         for j,fam2 in enumerate(similarProteins):
    #             if i >= j:
    #                 continue
    #             if not fam1.isdisjoint(fam2):
    #                 fam1 = fam1.union(fam2)
    #                 # lastSimProteins.append(fam1)
    #                 # foundMatch = True
    #         # if not foundMatch:
    #         lastSimProteins.append(fam1)
    #     if lastSimProteins != similarProteins:
    #         break
       
        # similarProteins = lastSimProteins
    oldNumFams = len(similarProteins)
    while True:
        restart = False
        print(len(similarProteins))
        for i,fam1 in enumerate(similarProteins):
            for j,fam2 in enumerate(similarProteins):
                if i >= j:
                    continue
                if not fam1.isdisjoint(fam2):
                    similarProteins[i] = fam1.union(fam2)
                    similarProteins.pop(j)
                    restart = True
                    break
            if restart:
                break
        if not restart:
            break
        
    print(similarProteins)
    with open("clusters", "w") as out:

        print(similarProteins,file=out)
     

