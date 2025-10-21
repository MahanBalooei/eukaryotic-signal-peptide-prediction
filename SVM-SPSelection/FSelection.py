import pandas as pd
import numpy as np
import requests
from io import StringIO
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from collections import Counter

# Constants
AMINO_ACIDS = list('ACDEFGHIKLMNPQRSTVWY')
KD_SCALE = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}
CHOU_FASMAN = {
    'A': (1.42, 0.83, 0.66), 'R': (0.98, 0.93, 0.95), 'N': (0.67, 0.89, 1.56),
    'D': (1.01, 0.54, 1.46), 'C': (0.70, 1.19, 1.19), 'Q': (1.11, 1.10, 0.98),
    'E': (1.51, 0.37, 0.74), 'G': (0.57, 0.75, 1.56), 'H': (1.00, 0.87, 0.95),
    'I': (1.08, 1.60, 0.47), 'L': (1.21, 1.30, 0.59), 'K': (1.16, 0.74, 1.01),
    'M': (1.45, 1.05, 0.60), 'F': (1.13, 1.38, 0.60), 'P': (0.57, 0.55, 1.52),
    'S': (0.77, 0.75, 1.43), 'T': (0.83, 1.19, 0.96), 'W': (1.08, 1.37, 0.96),
    'Y': (0.69, 1.47, 1.14), 'V': (1.06, 1.70, 0.50)
}

# Functions
def load_data(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t')
    df.columns = df.columns.str.strip()
    df['label'] = pd.to_numeric(df['label'], errors='coerce').fillna(0).astype(int)
    return df

def fetch_sequences(accessions, batch_size=50):
    sequences = {}
    for i in range(0, len(accessions), batch_size):
        batch = accessions[i:i + batch_size]
        query = ' OR '.join(f'accession:{acc}' for acc in batch)
        url = f'https://rest.uniprot.org/uniprotkb/search?format=fasta&query={query.replace(" ", "%20")}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            for record in SeqIO.parse(StringIO(response.text), 'fasta'):
                acc = record.id.split('|')[1] if '|' in record.id else record.id
                sequences[acc] = str(record.seq).upper()
        except Exception as e:
            print(f"❌ Fetch error: {e}")
    return sequences

def compute_aa_composition(seq, window_size=22):
    if not seq: return np.zeros(len(AMINO_ACIDS))
    prefix = seq[:window_size] if len(seq) >= window_size else seq
    counts = Counter(prefix)
    total = len(prefix)
    return np.array([counts.get(aa, 0) / total for aa in AMINO_ACIDS])

def compute_other_features(seq, prefix_len=40):
    if not seq: return np.zeros(6)
    prefix = seq[:prefix_len]
    if len(prefix) < 3: return np.zeros(6)

    pos_fraction = (prefix[:5].count('K') + prefix[:5].count('R')) / 5
    try:
        analysis = ProteinAnalysis(prefix)
        mw = analysis.molecular_weight() / len(prefix)
        charge = analysis.charge_at_pH(7.0)
    except:
        mw = 0.0
        charge = 0.0

    counts = Counter(prefix)
    total = len(prefix)
    helix = sum((counts.get(aa, 0) / total) * cf[0] for aa, cf in CHOU_FASMAN.items())
    sheet = sum((counts.get(aa, 0) / total) * cf[1] for aa, cf in CHOU_FASMAN.items())
    coil  = sum((counts.get(aa, 0) / total) * cf[2] for aa, cf in CHOU_FASMAN.items())
    return np.array([pos_fraction, mw, charge, helix, sheet, coil])

def compute_hydro_features(seq, kd_scale, window_size=5, prefix_len=40):
    if not seq or len(seq) < window_size: return np.array([0.0, 0.0])
    prefix = seq[:prefix_len]
    profile = [
        np.mean([kd_scale.get(aa, 0) for aa in prefix[i:i+window_size]])
        for i in range(len(prefix) - window_size + 1)
    ]
    return np.array([np.mean(profile), np.max(profile)])

# === MAIN ===
if __name__ == "__main__":
    df = load_data("training_with_folds.tsv")
    accessions = df['Accession'].dropna().unique().tolist()
    sequences = fetch_sequences(accessions)

    # Attach sequences
    df['Sequence'] = df['Accession'].map(sequences)
    df = df.dropna(subset=['Sequence'])

    # Feature extraction
    df['aa_comp'] = df['Sequence'].apply(lambda s: compute_aa_composition(s))
    df['other']   = df['Sequence'].apply(lambda s: compute_other_features(s))
    df['hydro']   = df['Sequence'].apply(lambda s: compute_hydro_features(s, KD_SCALE))

    # Final feature matrix
    X = np.hstack([np.stack(df['aa_comp']), np.stack(df['other']), np.stack(df['hydro'])])
    feature_names = (
        AMINO_ACIDS +
        ['pos_fraction_N5', 'molecular_weight', 'net_charge', 'helix_prop', 'sheet_prop', 'coil_prop'] +
        ['avg_hydro', 'max_hydro']
    )

    # Build DataFrame and include Accession
    df_features = pd.DataFrame(X, columns=feature_names)
    df_features['Accession'] = df['Accession'].values  # ✅ Fix that enables merge

    # Save
    df_features.to_csv('features.csv', index=False)
    print("✅ features.csv saved with Accession and all features.")
