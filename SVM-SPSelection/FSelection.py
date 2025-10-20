import pandas as pd
import numpy as np
import requests
from io import StringIO
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from collections import Counter

# Amino acids and KD scale
AMINO_ACIDS = list('ACDEFGHIKLMNPQRSTVWY')
KD_SCALE = {
    'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
    'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
    'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
    'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2
}

# Chou-Fasman propensities (P_alpha, P_beta, P_turn; normalized 0-1 for % est)
CHOU_FASMAN = {
    'A': (1.42, 0.83, 0.66), 'R': (0.98, 0.93, 0.95), 'N': (0.67, 0.89, 1.56),
    'D': (1.01, 0.54, 1.46), 'C': (0.70, 1.19, 1.19), 'Q': (1.11, 1.10, 0.98),
    'E': (1.51, 0.37, 0.74), 'G': (0.57, 0.75, 1.56), 'H': (1.00, 0.87, 0.95),
    'I': (1.08, 1.60, 0.47), 'L': (1.21, 1.30, 0.59), 'K': (1.16, 0.74, 1.01),
    'M': (1.45, 1.05, 0.60), 'F': (1.13, 1.38, 0.60), 'P': (0.57, 0.55, 1.52),
    'S': (0.77, 0.75, 1.43), 'T': (0.83, 1.19, 0.96), 'W': (1.08, 1.37, 0.96),
    'Y': (0.69, 1.47, 1.14), 'V': (1.06, 1.70, 0.50)
}

def load_data(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t')
    df.columns = df.columns.str.strip()
    df['SP cleavage'] = pd.to_numeric(df['SP cleavage'], errors='coerce')
    df['SP_length'] = (df['SP cleavage'] - 1).fillna(0)
    df['label'] = pd.to_numeric(df['label'], errors='coerce').fillna(0).astype(int)
    df['fold'] = pd.to_numeric(df['fold'], errors='coerce').fillna(-1).astype(int)
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
            print(f"Fetch error for batch {i//batch_size + 1}: {e}")
    return sequences

def compute_aa_composition(seq, window_size=22):
    if not seq or len(seq) == 0:
        return np.zeros(len(AMINO_ACIDS))
    if len(seq) < window_size:
        counts = Counter(seq)
        total = len(seq)
    else:
        prefix = seq[:window_size]
        counts = Counter(prefix)
        total = window_size
    return np.array([counts.get(aa, 0) / total for aa in AMINO_ACIDS])

def compute_other_features(seq, prefix_len=40):
    if not seq or len(seq) == 0:
        return np.zeros(6)  # pos_frac, MW, net_charge, helix, sheet, coil
    prefix = seq[:prefix_len]
    if len(prefix) < 3:
        return np.zeros(6)
    
    # Pos fraction N5
    prefix_pos = seq[:5]
    pos_fraction = (prefix_pos.count('K') + prefix_pos.count('R')) / len(prefix_pos) if len(prefix_pos) > 0 else 0.0
    
    # MW and net charge via ProtParam
    try:
        analysis = ProteinAnalysis(prefix)
        molecular_weight = analysis.molecular_weight() / len(prefix) if len(prefix) > 0 else 0.0  # Avg MW per residue
        net_charge = analysis.charge_at_pH(7.0)  # Full net charge at neutral pH
    except:
        molecular_weight = 0.0
        net_charge = 0.0
    
    # Secondary structure propensities (weighted % est)
    counts = Counter(prefix)
    total = len(prefix)
    helix_sum = sum((counts.get(aa, 0) / total) * chou[0] for aa, chou in CHOU_FASMAN.items())
    sheet_sum = sum((counts.get(aa, 0) / total) * chou[1] for aa, chou in CHOU_FASMAN.items())
    coil_sum = sum((counts.get(aa, 0) / total) * chou[2] for aa, chou in CHOU_FASMAN.items())
    # Normalize to [0,1] (rough %; sum ~3, but we keep raw weighted for now—scale if needed)
    helix_prop = helix_sum / max(helix_sum, 1.0)
    sheet_prop = sheet_sum / max(sheet_sum, 1.0)
    coil_prop = coil_sum / max(coil_sum, 1.0)
    
    return np.array([pos_fraction, molecular_weight, net_charge, helix_prop, sheet_prop, coil_prop])

def compute_hydro_features(seq, kd_scale, window_size=5, prefix_len=40):
    if not seq or len(seq) < window_size:
        return np.array([0.0, 0.0])
    prefix = seq[:prefix_len]
    if len(prefix) < window_size:
        return np.array([0.0, 0.0])
    profile = [np.mean([kd_scale.get(aa, 0) for aa in prefix[i:i + window_size]]) for i in range(len(prefix) - window_size + 1)]
    return np.array([np.mean(profile), np.max(profile)])

if __name__ == "__main__":
    df = load_data('training_with_folds.tsv')
    accessions = df['Accession'].unique().tolist()
    sequences = fetch_sequences(accessions)
    df['Sequence'] = df['Accession'].map(sequences)
    df = df.dropna(subset=['Sequence'])
    
    df['aa_comp'] = df['Sequence'].apply(lambda s: compute_aa_composition(s))
    df['other'] = df['Sequence'].apply(lambda s: compute_other_features(s))
    df['hydro'] = df['Sequence'].apply(lambda s: compute_hydro_features(s, KD_SCALE))
    
    X = np.hstack([np.stack(df['aa_comp']), np.stack(df['other']), np.stack(df['hydro'])])
    feature_names = AMINO_ACIDS + ['pos_fraction_N5', 'molecular_weight', 'net_charge', 'helix_prop', 'sheet_prop', 'coil_prop', 'avg_hydro', 'max_hydro']
    
    df_features = pd.DataFrame(X, columns=feature_names)
    df_features.to_csv('features.csv', index=False)
    
    print("✅ CSV saved as features.csv (29 features: 20 AA + SP + 6 other + 2 hydro)")
    print(df_features.head())