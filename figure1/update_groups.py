from Bio import SeqIO
import concurrent.futures
import os
import pickle

def extract_sequences(fasta_file):
    sequences = {}
    with open(fasta_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            sequences[record.id] = str(record.seq)
    return sequences

def gen_fasta(group_id, matching_ids, protein_seqs):
    with open(f"completeLinkageGroups-update/{group_id}", "w") as file:
        for i in matching_ids:
            file.write(f">{i}\n")
            file.write(f"{protein_seqs[str(i)]}\n")


if __name__ == "__main__":
    with open('temp.pkl', 'rb') as file:
        data = pickle.load(file)

    protein_seqs_ids = list(data.keys())
    protein_seqs = extract_sequences("combinedProteins.fasta")

    workers = int(os.environ.get('SLURM_CPUS_PER_TASK', 16))

    with concurrent.futures.ThreadPoolExecutor(max_workers = workers) as executor:
        futures = []
        for i in protein_seqs_ids:
            futures.append(executor.submit(gen_fasta, i, data[i], protein_seqs))

        for future in concurrent.futures.as_completed(futures):
            future.result()
