import pandas as pd
import numpy as np
import requests
from io import StringIO
from Bio import SeqIO
from collections import Counter
from sklearn.metrics import precision_recall_curve, f1_score, roc_curve, auc
import matplotlib.pyplot as plt

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

# --- Background frequencies ---
SWISSPROT_FREQ = {
    'A': 0.0825, 'C': 0.0138, 'D': 0.0546, 'E': 0.0671, 'F': 0.0386,
    'G': 0.0707, 'H': 0.0227, 'I': 0.0590, 'K': 0.0579, 'L': 0.0964,
    'M': 0.0241, 'N': 0.0406, 'P': 0.0474, 'Q': 0.0393, 'R': 0.0552,
    'S': 0.0665, 'T': 0.0536, 'V': 0.0685, 'W': 0.0110, 'Y': 0.0292
}
AA_LIST = sorted(SWISSPROT_FREQ.keys())

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
print(f"Folds: {df['fold'].value_counts().sort_index()}")

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

# --- Predict SP score ---
def predict_sp_score(seq, log_odds, min_cleavage=15, max_cleavage=100):
    scores = []
    aa_idx = {aa: i for i, aa in enumerate(AA_LIST)}
    for k in range(min_cleavage, min(max_cleavage + 1, len(seq) - 2)):
        context = extract_context(seq, k)
        if context is None:
            continue
        score = 0
        for i, aa in enumerate(context):
            score += log_odds[i, aa_idx.get(aa, 0)] if aa in aa_idx else -10
        scores.append(score)
    return max(scores) if scores else float('-inf')

# --- Cross-validation with PR + ROC ---
def run_cross_validation(df):
    folds = sorted(df['fold'].unique())
    all_scores = []
    all_labels = []
    thresholds = []
    f1_scores = []
    
    for test_fold in folds:
        train_df = df[df['fold'] != test_fold]
        log_odds, n_train = build_von_heijne_model(train_df)
        test_df = df[df['fold'] == test_fold]
        fold_scores = []
        fold_labels = test_df['label'].tolist()
        for _, row in test_df.iterrows():
            seq = row['Sequence']
            score = predict_sp_score(seq, log_odds)
            fold_scores.append(score)
        all_scores.extend(fold_scores)
        all_labels.extend(fold_labels)
        prec, rec, thresh = precision_recall_curve(fold_labels, fold_scores)
        f1 = 2 * prec * rec / (prec + rec + 1e-8)
        best_idx = np.argmax(f1)
        best_thresh = thresh[best_idx]
        thresholds.append(best_thresh)
        f1_scores.append(f1[best_idx])
        print(f"Fold {test_fold}: Trained on {n_train}, Best thresh={best_thresh:.3f}, F1={f1_scores[-1]:.3f}")
    
    avg_thresh = np.mean(thresholds)
    preds = (np.array(all_scores) > avg_thresh).astype(int)
    overall_f1 = f1_score(all_labels, preds)
    print(f"Average threshold: {avg_thresh:.3f}")
    print(f"Overall CV F1: {overall_f1:.3f}")

    # --- PR Curve ---
    prec, rec, _ = precision_recall_curve(all_labels, all_scores)
    plt.figure(figsize=(8, 6))
    plt.plot(rec, prec, label='PR Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Cross-Validation PR Curve')
    plt.legend()
    plt.savefig('cv_pr_curve.png')
    plt.show()

    # --- ROC Curve ---
    fpr, tpr, _ = roc_curve(all_labels, all_scores)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], 'k--', label='Random')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Cross-Validation ROC Curve')
    plt.legend()
    plt.savefig('cv_roc_curve.png')
    plt.show()

    return avg_thresh, overall_f1

# --- Run ---
avg_threshold, cv_f1 = run_cross_validation(df)