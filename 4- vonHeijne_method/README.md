# Step 4 — Von Heijne Signal Peptide Classifier
**LB2 Project · Group 7 · Signal Peptide Prediction**

## Overview

This folder contains the implementation and results for the Von Heijne method of signal peptide (SP) detection. The classifier uses a Position-Specific Weight Matrix (PSWM) built from log-odds amino acid frequencies around the cleavage site window.

## Contents

| File | Description |
|------|-------------|
| `step4_von_heijne.ipynb` | Main notebook — full pipeline from data loading to evaluation |
| `figures/vh_pswm_heatmap.pdf/.png` | PSWM log-odds weights heatmap (positions −13 to +2) |
| `figures/vh_cv_pr_roc.pdf/.png` | 5-fold cross-validation PR and ROC curves |
| `figures/vh_benchmark_confusion.pdf/.png` | Benchmark confusion matrix |

## Method

1. **Window extraction** — a 15-position window (positions **−13 to +2** relative to the cleavage site) is extracted from each positive training sequence.
2. **PSWM construction** — log-odds scores are computed against SwissProt background amino acid frequencies, with pseudocount = 1.0 for smoothing.
3. **Scoring** — each protein is scored by sliding the PSWM over N-terminal positions 15–100 and taking the maximum score.
4. **Threshold selection** — 5-fold cross-validation is used; per fold, the threshold maximising F1 on the OOF PR curve is selected. The average OOF threshold (6.339) is then applied to the benchmark set.
5. **Final model** — retrained on the full training set (873 positive sequences) and evaluated on the blind benchmark set.

## Input Files (from previous steps)

| File | Description |
|------|-------------|
| `filtered_positive.tsv` | Clustered positive representatives (Step 2) |
| `filtered_negative.tsv` | Clustered negative representatives (Step 2) |
| `training_with_folds.tsv` | Training set with label and 5-fold assignment columns |
| `benchmarking_set.tsv` | Blind benchmark set with label column |
| `positive.fasta` / `negative.fasta` | Source protein sequences (filtered accessions only) |

> **Note:** All sequences were restricted to the filtered non-redundant set produced in Step 2 before training and evaluation.

## Results

### Model Parameters

| Parameter | Value |
|-----------|-------|
| Window size | 15 positions (−13 to +2) |
| Pseudocount | 1.0 |
| Background frequencies | SwissProt (ExPASy) |
| Cleavage site search range | positions 15–100 |
| Training positives | 873 |
| OOF threshold | 6.339 |

### Performance

| Metric | 5-fold CV | Benchmark |
|--------|----------:|----------:|
| Accuracy | 0.935 | 0.922 |
| Precision | 0.686 | 0.625 |
| Recall | 0.736 | 0.717 |
| F1 | 0.710 | 0.668 |
| MCC | 0.674 | 0.626 |

### Benchmark Confusion Matrix

|  | Predicted SP− | Predicted SP+ |
|--|-------------:|-------------:|
| **Actual SP−** | 1693 (TN) | 94 (FP) |
| **Actual SP+** | 62 (FN) | 157 (TP) |

### Cross-Validation Curves

- **PR AUC:** 0.782
- **ROC AUC:** 0.954
- OOF threshold point: F1 = 0.710 at recall ≈ 0.74, precision ≈ 0.69

## Dependencies

```
biopython
pandas
numpy
scikit-learn
matplotlib
seaborn
```

Install with:
```bash
pip install biopython pandas numpy scikit-learn matplotlib seaborn
```

## Usage

Open and run `step4_von_heijne.ipynb` cell by cell. Ensure the input `.tsv` and `.fasta` files from Step 2 are available in the working directory. Output figures are saved to the `figures/` subdirectory.
