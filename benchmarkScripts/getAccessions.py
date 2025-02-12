
import sys
import os


def getSecondCol(path):
    acessionsToDownload = []
    with open(path) as file:
        for line in file:
            line = line.strip()
            cols = line.split("\t")
            if len(cols) < 2:
                continue
            acessionsToDownload.append(cols[1])
    return acessionsToDownload

outputPathPrefix = "./annotationFiles/"
accessionFilePath = "PhagesDB_accession_numbers.txt"


if __name__ == "__main__":
    if not os.path.exists(outputPathPrefix):
        os.mkdir(outputPathPrefix)
    accessions = getSecondCol(accessionFilePath)
    # url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id="  # + contigName + "&retType=gb"
    with open("accessions.txt","w") as outfile:
        for accession in accessions:
            outfile.write(accession + "\n")
        
