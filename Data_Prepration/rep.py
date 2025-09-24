from Bio import SeqIO

# For positive
positive_reps = [record.id for record in SeqIO.parse('cluster-results1_rep_seq.fasta', 'fasta')]
print(f"Positive representatives: {len(positive_reps)}")

# For negative
negative_reps = [record.id for record in SeqIO.parse('cluster-results2_rep_seq.fasta', 'fasta')]
print(f"Negative representatives: {len(negative_reps)}")
with open('positive_reps.txt', 'w') as f:
    f.write('\n'.join(positive_reps))

with open('negative_reps.txt', 'w') as f:
    f.write('\n'.join(negative_reps))