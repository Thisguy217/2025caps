import requests
import json
import re

from time import *


def getAccessionsFromUniprotFile(accFileName):
    with open(accFileName) as file:
        lines = "\n".join(file.readlines())
        print(lines[:10])
        return re.findall(r">\w+\|(.+?)\|", lines)


accFileName = "/Users/cazcullimore/Downloads/c732434e62bbf5896cc80823de8bbf47e75af52d"
# url = "https://rest.uniprot.org/uniprotkb/search?query=ft_binding&fields=sequence&size=500"
# responseText = requests.get(url).text.rstrip()
# jsonText = json.loads(responseText)

# print("got results",len(jsonText["results"]))
accsToData = {}

# accs = getAccessionsFromUniprotFile(accFileName)
for acc in range(10):
    t1 = time()
    # acc = result['primaryAccession']
    acc = ""
    # seq = result["sequence"]["value"]
   
    url = "https://www.uniprot.org/uniprot/" + acc + ".txt"
    response = requests.get(url)
    proteinInfo = response.text.rstrip()
    print("start",proteinInfo,"stop")
    print(type(proteinInfo))
    bindingSites = re.findall("BINDING\s+([\d\.]+)\s+?FT\s+?.ligand=\"(.+?)\"",proteinInfo)
    re.findall("(evidence=)", proteinInfo)
    evidences = re.findall("ECO:0000269", proteinInfo)
    seq = "seq"#re.findall("ECO:0000269", proteinInfo)
    accsToData[acc] = [seq, bindingSites]
    print(time() - t1)
    # break # add 30mins 
with open("enzymeData.tsv","w") as out:
    print(accsToData,file=out)


