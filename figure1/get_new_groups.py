# Used to create a pickle that will then be used to update subsequent groups
import os
from Bio import SeqIO
from concurrent.futures import ProcessPoolExecutor
import itertools
from tqdm import tqdm
import pickle

def extract_sequences(fasta_file):
    sequences = {}
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            sequences[record.id] = str(record.seq)
    return sequences

def remove_sublists(groups):
    items = list(groups.items())
    keep = set(range(len(items)))

    #count = 0
    #temp = 0
    for i, (_, ids1) in enumerate(items):
        #count += 1
        for j, (_, ids2) in enumerate(items):
            if i != j and set(ids1).issubset(ids2):
                keep.discard(i)
                break
        #if temp < round(count/len(items)*100,0):
        #    temp = round(count/len(items)*100,0) 
        #    print(f"{temp}%")

    return {items[i][0]: items[i][1] for i in keep}

def remove_sublists_v2(groups, verbose=False):
    if not isinstance(groups, dict):
        raise TypeError("Input must be a dictionary")
    items = list(groups.items())
    keep = {}
    for i, (key1, ids1) in enumerate(items):
        is_subset = False
        
        for j, (_, ids2) in enumerate(items):
            if i != j and set(ids1).issubset(ids2):
                is_subset = True
                break
        
        if not is_subset:
            keep[key1] = ids1
        
        if verbose and i % max(1, len(items) // 10) == 0:
            print(f"{round(i/len(items)*100, 1)}%")
    
    return keep

if __name__ == "__main__":
    directory = 'singleLinkageGroups' #Point to new directory when running
    id_groups = {}
    if not os.path.exists('groups.pkl'):
        for i in tqdm(os.listdir(directory)):
            protein_seqs = extract_sequences(f"{directory}/{i}")
            id_groups[i] = list(protein_seqs.keys())
        
        with open('groups.pkl', 'wb') as file:
            pickle.dump(id_groups, file)
    else:
        with open('groups.pkl', 'rb') as file:
            id_groups = pickle.load(file)

    result = remove_sublists(id_groups)
    with open('temp.pkl', 'wb') as file:
        pickle.dump(result, file)
    print(result)
