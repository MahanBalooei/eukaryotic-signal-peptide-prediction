# Von Heijne Method

This folder implements the classical von Heijne signal peptide classifier as a rule-based baseline. A Position-Specific Weight Matrix (PSWM) is built from experimentally confirmed cleavage sites and used to score candidate cleavage positions across each protein's N-terminus. Performance is evaluated with 5-fold cross-validation and a final blind benchmark test.

---

## Contents

| File | Description |
|------|-------------|
| `step4_von_heijne.ipynb` | Full implementation: PSWM construction, CV, benchmark evaluation |
| `vh_pswm_heatmap.png/.pdf` | Log-odds weight matrix visualized as a heatmap (positions −13 to +2) |
| `vh_cv_pr_roc.png/.pdf` | PR and ROC curves from 5-fold cross-validation |
| `vh_benchmark_confusion.png/.pdf` | Confusion matrix on the blind benchmark set |

---

## Method

### 1 — Window extraction
A 15-residue window is extracted around each cleavage site in the positive training sequences: positions −13 to −1 (end of the signal peptide) and +1 to +2 (start of the mature protein). `SP cleavage` is 1-indexed; extraction uses 0-based Python indexing as `seq[cleavage−13 : cleavage+2]`.

### 2 — PSWM construction
A (15 × 20) log-odds matrix is computed from the extracted windows:

```
PSWM[pos][aa] = log( (count[pos][aa] + pseudocount) / total[pos] / swissprot_freq[aa] )
```

- Pseudocount: 1.0 (additive smoothing to handle zero counts)
- Background: SwissProt proteome-wide amino acid frequencies (ExPASy release statistics)

### 3 — Sequence scoring
Each protein is scored by sliding the PSWM over N-terminal positions 15–100 (candidate cleavage range) and taking the maximum score across all positions. This maximum score is the raw classifier output.

### 4 — 5-fold cross-validation
In each fold the PSWM is built on the four training folds (positive sequences only), then used to score the held-out validation fold. The threshold that maximises F1 on the per-fold PR curve is recorded. The final operating threshold is the average across all five folds, applied to the pooled CV scores for metric computation.

### 5 — Blind benchmark evaluation
The PSWM is retrained on the full training set. The average CV threshold is applied to benchmark sequences — sequences not seen during training or threshold selection — for the final unbiased performance estimate.

---

## Results

### 5-Fold Cross-Validation

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.954 |
| PR-AUC | 0.782 |
| F1 | 0.708 |

### Blind Benchmark (n = 2,006)

| | Predicted SP− | Predicted SP+ |
|---|---|---|
| **Actual SP−** | 1,691 (TN) | 96 (FP) |
| **Actual SP+** | 61 (FN) | 158 (TP) |

The PSWM heatmap confirms the expected biological signal: Ala is strongly enriched at positions −1 and −3 (von Heijne's −1/−3 rule), hydrophobic residues (Leu, Ile) dominate the central hydrophobic core (positions −13 to −6), and charged residues (Asp, Glu, Lys) are uniformly depleted throughout the SP window.

---

## Key Parameters

| Parameter | Value |
|-----------|-------|
| Window size | 15 positions (−13 to +2) |
| Pseudocount | 1.0 |
| Background frequencies | SwissProt (ExPASy) |
| Cleavage search range | positions 15–100 |
| Threshold selection | max F1 per fold, averaged across 5 folds |

---

## Input Files

Upload the following to Colab before running:

- `training_with_folds.tsv` — from `data_preparation/`
- `benchmarking_set.tsv` — from `data_preparation/`
- `positive.fasta` — from `data_collection/`
- `negative.fasta` — from `data_collection/`

---

## Dependencies

```
pip install biopython pandas numpy scikit-learn matplotlib seaborn
```
