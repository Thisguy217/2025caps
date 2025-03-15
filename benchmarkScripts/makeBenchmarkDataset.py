import json
import re
import subprocess
import os
import sys
from time import *
import re
# import pandas as pd
import requests
from glob import glob
from findConservedIndexes import *

# data = pd.read_csv("uniprotkb_ft_binding_experimental.tsv", sep="\t")

# print(data.iloc[1])

# oneProteinBindingData = data["Binding site"].iloc[1]
# # .apply(lambda x: x.split(";"))

# print(oneProteinBindingData)
# print("\n\n")

# bindingPos = re.findall(r'BINDING (\d+\.\.)?(\d+); /ligand="(.+?)".+?/evidence=".*?ECO:0000269.*?"', oneProteinBindingData)

# with open() # how to get structre
def getStructure(uniprotName):
    uniprotName = os.path.basename(uniprotName)
    structureName = uniprotName + ".pdb"
    with open(structureName,"w") as outfile:
        outfile.write(requests.get(f"https://alphafold.ebi.ac.uk/files/AF-" + uniprotName + "-F1-model_v4.pdb").text)

    return structureName

def getClusters(annotations):
    clusters = []
    clusterTypes = []
    for startIndex, stopIndex, ligandType, evidence in annotations:
        if startIndex == "":
            indicesToAdd = {int(stopIndex)}
        else:
            indicesToAdd = set(range(int(startIndex[:-2]), int(stopIndex)+1))


        overlappingClusterIndex = -1
        for index, cluster in enumerate(clusters):
            if not indicesToAdd.isdisjoint(cluster):
                overlappingClusterIndex = index
        if not ligandType in clusterTypes and overlappingClusterIndex == -1:
            clusterTypes.append(ligandType)
            clusters.append(indicesToAdd)
        else:
            if overlappingClusterIndex != -1:
                indexOfCluster = overlappingClusterIndex
            else:
                indexOfCluster = clusterTypes.index(ligandType)
            clusters[indexOfCluster].update(indicesToAdd)
    return clusters, clusterTypes

def countBindingSites(fileName):
    with open(fileName) as file:
        fileData = "".join([line.strip() for line in file.readlines()])
        bindingSites = len(re.findall("BINDING|ACT_SITE", fileData))
    return bindingSites


if __name__ == "__main__":
    outdata = []
    for proteinDir in glob("*/UniProt_Entries/"):
        groupName = proteinDir.split("/")[0]
        fileWithMostBindingSites = glob(proteinDir + "*txt")[0]
        maxBindingSites = countBindingSites(fileWithMostBindingSites)
        for file in glob(proteinDir + "*txt"):
            bindingSites = countBindingSites(file)
            if maxBindingSites < bindingSites:
                maxBindingSites = bindingSites
                fileWithMostBindingSites = file
        uniprotAcc = re.sub(".txt","",fileWithMostBindingSites)
        
        with open(fileWithMostBindingSites) as file:
            oneProteinBindingData = "".join([line.strip() for line in file.readlines()])

        bindingPos = re.findall(r'BINDING\s*(\d+\.\.)?(\d+).+?/ligand="(.+?)".+?/evidence=".*?(ECO:.*?)"', oneProteinBindingData)
        activePos = re.findall(r'ACT_SITE\s*(\d+\.\.)?(\d+)', oneProteinBindingData)
        uniprotSeq = re.findall(r'SEQUENCE.+;([\w\s]+)//', oneProteinBindingData)
        assert len(uniprotSeq) == 1
        uniprotSeq = uniprotSeq[0]
        uniprotSeq = uniprotSeq.replace(" ","")
        print(uniprotSeq)
        alphafoldAcc = re.findall("AlphaFoldDB; ([\w\d]+);", oneProteinBindingData)
        print(uniprotAcc, alphafoldAcc)
        # assert len(alphafoldAcc) <= 1
        # alphafoldAcc = alphafoldAcc[0]
        structureName = getStructure(uniprotAcc)

        clusters, clusterTypes = getClusters(bindingPos)

        # add active size cluster assuming that there is a single active site cluster
        activeSiteIndices = set()
        for startIndex, stopIndex in activePos:
            if startIndex == "":
                indicesToAdd = {int(stopIndex)}
            else:
                indicesToAdd = set(range(int(startIndex[:-2]), int(stopIndex)+1))
            activeSiteIndices.update(indicesToAdd)

        addedToCluster = False
        # combine clusters
        for cluster in clusters:
            if not activeSiteIndices.isdisjoint(cluster):
                if addedToCluster:
                    print("WARNING: Tried to add active site to multiple clusters, only added to first cluster")
                    break

                cluster.update(activeSiteIndices)
                addedToCluster = True
        if not addedToCluster and len(activeSiteIndices) > 0:
            print("INFO: active site not part of any cluster")
            clusterTypes.append("activeSite")
            clusters.append(activeSiteIndices)
                
        conserved = getConservedIndexes(groupName + "/MSA/combined_fasta_sequences.afa", uniprotSeq)
        outdata.append((groupName,) + conserved[1:] + (clusters, clusterTypes,structureName))
        
        print(conserved)
    with open("dataset.tsv", "w") as outfile:
        outfile.write("groupName\tnumSeqs\tnumConserved\tMSAlength\tConservedIndices\trepresentativeSequence\tClusterIndices\tclusterLigands\tstructureFile\n")
        for fileOutData in outdata:
            print(*fileOutData,sep="\t",file=outfile)
            

