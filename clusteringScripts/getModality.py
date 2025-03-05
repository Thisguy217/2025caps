# import os
# import sys
# import numpy as np
# def readInFastaAsDict(fileName):
#     fileData = {}
#     with open(fileName) as file:
#         entryData = []
#         lastGenomeName = ""
#         for line in file:
#             if line[0] == ">":
#                 if entryData != []:
#                     fileData[lastGenomeName] = ''.join(entryData)
#                 lastGenomeName = line[1:].strip()
#                 entryData = []
#             else:
#                entryData.append(line.strip())
#         fileData[lastGenomeName] = ''.join(entryData)
#     return fileData

# def getExtremePoints(data, typeOfExtreme = None, maxPoints = None):
#     """
#     This method returns the indeces where there is a change in the trend of the input series.
#     typeOfExtreme = None returns all extreme points, max only maximum values and min
#     only min,
#     """
#     a = np.diff(data)
#     asign = np.sign(a)
#     signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
#     idx = np.where(signchange ==1)[0]
#     if typeOfExtreme == 'max' and data[idx[0]] < data[idx[1]]:
#         idx = idx[1:][::2]
#     elif typeOfExtreme == 'min' and data[idx[0]] > data[idx[1]]:
#         idx = idx[1:][::2]
#     elif typeOfExtreme is not None:
#         idx = idx[::2]
    
#     # sort ids by min value
#     if 0 in idx:
#         idx = np.delete(idx, 0)
#     if (len(data)-1) in idx:
#         idx = np.delete(idx, len(data)-1)
#     idx = idx[np.argsort(data[idx])]
#     # If we have maxpoints we want to make sure the timeseries has a cutpoint
#     # in each segment, not all on a small interval
#     if maxPoints is not None:
#         idx= idx[:maxPoints]
#         if len(idx) < maxPoints:
#             return (np.arange(maxPoints) + 1) * (len(data)//(maxPoints + 1))
    
#     return idx



# from unidip import UniDip

# # create bi-modal distribution
# dat = np.concatenate([np.random.randn(200)-3, np.random.randn(200)+3])

# # sort data so returned indices are meaningful
# dat = np.sort(dat)

# # get start and stop indices of peaks 
# intervals = UniDip(dat).run()

# # for fastaFile in sys.argv[1:]: 
# #     seqLengths = np.array([len(seq) for seq in readInFastaAsDict(fastaFile).values()])
# #     print(seqLengths)
    
# #    print(getExtremePoints(seqLengths))
    
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np
def make_data(N, f=0.3, rseed=1):
    rand = np.random.RandomState(rseed)
    x = rand.randn(N)
    x[int(f * N):] += 5
    return x

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

for fastaFile in ["/Users/cazcullimore/Downloads/group137055.fasta"]: 
    seqLengths = np.array([len(seq) for seq in readInFastaAsDict(fastaFile).values()])
    x = seqLengths
    x_d = np.linspace(min(seqLengths),max(seqLengths), 1000)
    print(x)
    density = sum(norm(xi).pdf(x_d) for xi in x)

    plt.fill_between(x_d, density, alpha=0.5)
    plt.plot(x, np.full_like(x, -0.1), '|k', markeredgewidth=1)

    for i in range(len(density) - 1):
        if density[i] > density[i+1] and density[i] > density[i-1]:
            print("max at",x_d[i]) 
    # plt.axis([-4, 8, -0.2, 5])
    plt.show()


        