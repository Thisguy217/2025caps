# import requests
import json
import re
import subprocess
import os
import sys
from time import *

# url = "http://hogenom.univ-lyon1.fr/query_sequence?seq=MRFQVIVAAATITMITSYIPGVASQSTSDGDDLFVPVSNFDPKSIFPEIKHPFEPMYANTENGKIVPTNSWISNLFYPSADNLAPTTPDPYTLRLLDGYGGNPGLTIRQPSAKVLGSYPPTNDVPYTDAGYMINSVVVDLRLTSSEWSDVVPDRQVTDWDHLSANLRLSTPQDSNSYIDFPIVRGMAYITANYNNLTPQFLSQHAIISVEADEKKSDDNTSTFSGRKFKITMNDDPTSTFIIYSLGDKPLELRKQDNSNLVASKPYTGVIRVAKLPAPEFETLLDASRAVWPTGGDISARSDDNNGASYTIKWKTNSNEAPLLTYAYAHHLTSIDDSNVKRTDMTLQSATKGPMTALVGNEWTLRETELSPVEWLPLQAAPNPTTINEIMTEINKDIASNYTQETAKEDNYFSGKGLQKFAMLALILNKSDQTQLRNPELAQIALDKLKAAFLPYLQNEQADPFRYDTLYKGIVAKAGLPTSMGGTDDLSAEFGHSYYSDHHYHQGYFVVTAAIIHHLDPTWNADRLKAWTEALIRDVNNANDGDEYFAAFRNWDWFAGHSWAGGIKPDGALDGRDQESVPESVNFYWGAKLWGLATGNTPLTKLASLQLAVTKRTTYEYFWMLDGNKNRPENIVRNKVIGIYFEQKTDYTTYFGRFLEYIHGIQQLPMTPELMEYIRTPEFVSQEWDEKLGAIAPTVQSPWAGVLYLNYAIINPAEAYPALRKVQMDDGQTRSYSLYLTATRPHFFRRSLLAALARHGSTRRPSLPSSGDDDKHEDGFLLRFRRLNPFNLKHRIY"
# url = "http://hogenom.univ-lyon1.fr/query_sequence?seq=MQAETILEGLEAGLPQAVSSGLSLVPAPGLVLTCLSAPSGPGGMALEPPPTTLRKAFLAQSTLLESTLEGAPEWAAPHPEEQRRSPPACSQHTPPLPSTPTGPPPCSPGGNHPLCALSGRGGGRCSIPSLSSSSTFSLFSSGCWNPRVKLRVRKSQSQGRAGQLI"
# response = requests.get(url)

# print(response)
# proteinInfo = response.text.rstrip()

# print(proteinInfo)

def runBlast(queryFile,dbPath,outFile):
    with open(outFile,"a") as out:
        subprocess.run(("blastp -query " + queryFile + " -db " + dbPath + " -outfmt 6").split(), stdout=out)


if __name__ == "__main__":
    assignedQueryFileName = sys.argv[1]
    subjectFileName = sys.argv[2]
    try:
        blastOutputFileName = sys.argv[3]
    except IndexError:
        blastOutputFileName = "blastOut.tsv"

    header = "query acc.ver\tsubject acc.ver\t% identity\talignment length\tmismatches\tgap opens\tq. start\tq. end\ts. start\ts. end\tevalue\tbit score\n"
    if not os.path.exists(blastOutputFileName):
        with open(blastOutputFileName, "w") as out:
            out.write(header)

    runBlast(assignedQueryFileName,subjectFileName, blastOutputFileName)