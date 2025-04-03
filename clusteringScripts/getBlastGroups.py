import pandas as pd
import sys
import pickle

if __name__ == "__main__":

    blastOutputFileName = sys.argv[1]
    blastOutput = pd.read_csv(blastOutputFileName, sep="\t")
    
    queryNames = set(blastOutput["query acc.ver"].tolist())
    similarProteins = []
    for name in queryNames:
        famForThisProtein = set(blastOutput.loc[blastOutput["query acc.ver"] == name].loc[blastOutput["evalue"] < 1e-10]["subject acc.ver"].tolist())
        similarProteins.append(famForThisProtein)
    
    with open("clusterGroups.p","wb") as out:
        pickle.dump(similarProteins,out)
