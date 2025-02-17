import pandas as pd
from copy import deepcopy
import sys
import random
from time import *

def combineClusters(connectedProteins, proteinNames):


    # currentClusters = {i:i for i in range(0,numProteins)}


    # proteinsMatchingAll = connectedProteins[list(currentClusters)[0]]
    currentClusters = {}
    t1 = time()
    for i, startingProtein in enumerate(proteinNames):
        if i % 1000 == 0:
            print(i/len(list(proteinNames)), (time() - t1) / (i+1) * len(list(proteinNames)))
            t1 = time()
        currentCluster = {startingProtein}
        for connectedProtein in connectedProteins[startingProtein]: # original
            connectedToAllMembers = True
            for connectedProtein2 in deepcopy(currentCluster):
                if not connectedProtein in connectedProteins[connectedProtein2]:
                    connectedToAllMembers = False
                    break
            if connectedToAllMembers:
                currentCluster.add(connectedProtein)
        # print("cc",currentCluster)
        currentClusters[startingProtein] = currentCluster
    return currentClusters
def test():
    p = {1:{1,2,3,4,5}, 2:{2,3,9,8}, 0:{0},3:{3},4:{4},5:{5},8:{8},9:{9}}
    out = combineClusters(p,p.keys())
    print(out)
    assert [{0, 10, 20, 30}, {1, 2, 3, 4, 5, 8, 9}] == out or [ {1, 2, 3, 4, 5, 8, 9},{0, 10, 20, 30}] == out

def testAll(groups, connections):
    for group in groups:
        for protein1 in group:
            for protein2 in group:
                assert protein2 in connections[protein1]
if __name__ == "__main__":

    isTesting = False
    if not isTesting:
        # blastOutputFileName = sys.argv[1]#"blastOut.tsv"
        blastOutputFileName = "/Users/cazcullimore/Downloads/allGBProteinsPairwiseBlast.tsv" #"smallPairwiseBlast.tsv"
        blastOutput = pd.read_csv(blastOutputFileName, sep="\t")
        
        print(blastOutput.columns)
        print(blastOutput)
        queryNames = set(blastOutput["query acc.ver"].tolist())
        connectedProteins = {}
        for name in queryNames:
            famForThisProtein = set(blastOutput.loc[blastOutput["query acc.ver"] == name].loc[blastOutput["evalue"] < 1e-10]["subject acc.ver"].tolist())
            connectedProteins[name] = famForThisProtein
        
        finalGroups = combineClusters(connectedProteins, connectedProteins.keys())
        testAll(finalGroups, connectedProteins)
        print(finalGroups)

    else:
        test()
        # testRandom()