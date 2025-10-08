import pandas as pd
import numpy as np
import requests
from io import StringIO
from Bio import SeqIO
from collections import Counter
import matplotlib.pyplot as plt

# --- Background frequencies ---
SWISSPROT_FREQ = {
    'A': 0.0825, 'C': 0.0138, 'D': 0.0546, 'E': 0.0671, 'F': 0.0386,
    'G': 0.0707, 'H': 0.0227, 'I': 0.0590, 'K': 0.0579, 'L': 0.0964,
    'M': 0.0241, 'N': 0.0406, 'P': 0.0474, 'Q': 0.0393, 'R': 0.0552,
    'S': 0.0665, 'T': 0.0536, 'V': 0.0685, 'W': 0.0110, 'Y': 0.0292
}
AA_LIST = sorted(SWISSPROT_FREQ.keys())

# --- Fetch UniProt sequences ---
def fetch_sequences(accessions, batch_size=100):
    sequences = {}
    for i in range(0, len(accessions), batch_size):
        batch = accessions[i:i + batch_size]
        query = '%20OR%20'.join(f'accession:{acc}' for acc in batch)
        url = f'https://rest.uniprot.org/uniprotkb/stream?format=fasta&query={query}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            for record in SeqIO.parse(StringIO(response.text), 'fasta'):
                acc = record.id.split('|')[1] if '|' in record.id else record.id
                sequences[acc] = str(record.seq)
        except Exception as e:
            print(f"Batch failed: {e}")
    print(f"Fetched {len(sequences)} sequences")
    return sequences

# --- Load data ---
df = pd.read_csv('training_with_folds.tsv', sep='\t')
df.columns = df.columns.str.strip()
df['SP cleavage'] = pd.to_numeric(df['SP cleavage'], errors='coerce')
df['label'] = pd.to_numeric(df['label'], errors='coerce').fillna(0).astype(int)
df['fold'] = pd.to_numeric(df['fold'], errors='coerce').fillna(-1).astype(int)

# --- Fetch sequences ---
all_accessions = df['Accession'].unique().tolist()
all_seqs = fetch_sequences(all_accessions)
df['Sequence'] = df['Accession'].map(all_seqs)
df = df.dropna(subset=['Sequence'])

print(f"Total samples: {len(df)}, Positives: {sum(df['label'])}, Negatives: {len(df) - sum(df['label'])}")

# --- Extract context ---
def extract_context(seq, cleavage):
    if pd.isna(cleavage) or len(seq) < cleavage + 2:
        return None
    start_idx = int(cleavage) - 14
    end_idx = int(cleavage) + 1
    context = seq[start_idx:end_idx]
    if len(context) != 15:
        return None
    return context

# --- Build Von Heijne model ---
def build_von_heijne_model(pos_df, pseudocount=1):
    pos_list = pos_df[pos_df['label'] == 1]
    counts = {pos: Counter() for pos in range(15)}
    n_pos = 0
    for _, row in pos_list.iterrows():
        context = extract_context(row['Sequence'], row['SP cleavage'])
        if context is not None:
            for i, aa in enumerate(context):
                counts[i][aa] += 1
            n_pos += 1
    if n_pos == 0:
        raise ValueError("No valid positives!")
    pos_freq = np.zeros((15, 20))
    aa_idx = {aa: i for i, aa in enumerate(AA_LIST)}
    for pos in range(15):
        total_count = sum(counts[pos].values()) + 20 * pseudocount
        for aa in AA_LIST:
            count = counts[pos].get(aa, 0) + pseudocount
            pos_freq[pos, aa_idx[aa]] = count / total_count
    log_odds = np.log(pos_freq / np.array([SWISSPROT_FREQ[aa] for aa in AA_LIST]))
    log_odds = np.nan_to_num(log_odds, nan=-10)
    return log_odds, n_pos

# --- Visualize log-odds weights as heatmap (using all positives) ---
pos_df = df[df['label'] == 1]
log_odds, n_pos = build_von_heijne_model(pos_df)
print(f"Built model from {n_pos} positive examples")

fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(log_odds, cmap='RdBu_r', aspect='auto', vmin=-3, vmax=3)

# Labels
ax.set_xticks(np.arange(len(AA_LIST)))
ax.set_xticklabels(AA_LIST, rotation=45, ha='right')
positions = [f'-{14 - i}' if i < 14 else '+1' for i in range(15)]
ax.set_yticks(np.arange(15))
ax.set_yticklabels(positions)

# Colorbar and labels
cbar = plt.colorbar(im, ax=ax, label='Log Odds Ratio')
plt.title(f'Von Heijne Log-Odds Weight Matrix\n(Built from {n_pos} positives)')
plt.xlabel('Amino Acid')
plt.ylabel('Position Relative to Cleavage Site\n(-1: last SP residue; +1: first mature residue)')

plt.tight_layout()
plt.savefig('von_heijne_weights_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()