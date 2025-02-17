import pandas as pd
from copy import deepcopy
import sys
import random

def combineClusters(similarProteins):
    
    directConnections = {}
    for i,fam1 in enumerate(similarProteins):
            print(i/len(similarProteins), "progress making connections")
            for j,fam2 in enumerate(similarProteins):
                if i == j:
                    continue
                if not fam1.isdisjoint(fam2):
                    if i not in directConnections.keys():
                        directConnections[i] = set()
                    directConnections[i].add(j)

    groupsUnvisited = set(range(len(similarProteins)))
    groupsWithNoConnections = groupsUnvisited.difference(set(directConnections.keys()))
    groupsUnvisited = set(directConnections.keys())
    finalGroups = [similarProteins[g] for g in groupsWithNoConnections]
    print("found connections")

    while groupsUnvisited:

        
        currentGroupIndex = groupsUnvisited.pop() # 0 

        currentGroup = similarProteins[currentGroupIndex] # 1

        groupsToVisit = set(directConnections[currentGroupIndex]) # {1}
        while groupsToVisit:
            connectionIndex = groupsToVisit.pop()
            if not connectionIndex in groupsUnvisited:
                continue
            groupsUnvisited.remove(connectionIndex)
            groupsToVisit = groupsToVisit.union(set(directConnections[connectionIndex]))
            currentGroup = currentGroup.union(similarProteins[connectionIndex])
        finalGroups.append(currentGroup)
    return finalGroups

def test():
    p = [{1,2,3,4,5}, {2,3,9,8}, {0,10,20,30}]
    out = combineClusters(p)

    assert [{0, 10, 20, 30}, {1, 2, 3, 4, 5, 8, 9}] == out or [ {1, 2, 3, 4, 5, 8, 9},{0, 10, 20, 30}] == out

def bruteForce(similarProteinsArg):
    similarProteins = deepcopy(similarProteinsArg)
    while True:
        restart = False
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
            return similarProteins
def testRandom():
    numTests = 100
    for _ in range(numTests):
        numGroups = 200
        p = [{random.randint(0,10000) for _ in range(10)} for _ in range(numGroups)]
        brutOut = bruteForce(p)
        brutOut.sort(key=lambda a: sum(a))
        clusterOut = combineClusters(p)
        clusterOut.sort(key=lambda a: sum(a))
        assert len(brutOut) == len(clusterOut)
        for i,group in enumerate(brutOut):
            if len(group.difference(clusterOut[i])) > 0 or len(clusterOut[i].difference(group)) > 0:
                raise Exception((brutOut,clusterOut))
if __name__ == "__main__":

    isTesting = False
    if not isTesting:
        # blastOutputFileName = sys.argv[1]#"blastOut.tsv"
        blastOutputFileName = "~/Downloads/allGBProteinsPairwiseBlast.tsv" #"smallPairwiseBlast.tsv"
        blastOutput = pd.read_csv(blastOutputFileName, sep="\t")
        
        print(blastOutput.columns)
        print(blastOutput)
        queryNames = set(blastOutput["query acc.ver"].tolist())
        similarProteins = []
        for name in queryNames:
            famForThisProtein = set(blastOutput.loc[blastOutput["query acc.ver"] == name].loc[blastOutput["evalue"] < 1e-10]["subject acc.ver"].tolist())
            similarProteins.append(famForThisProtein)
        
        finalGroups = combineClusters(similarProteins)
        print(finalGroups)

    else:
        test()
        testRandom()