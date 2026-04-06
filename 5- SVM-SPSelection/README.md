# SVM Classifier

This folder implements a Support Vector Machine (SVM) classifier for signal peptide detection using biochemical features extracted from protein N-termini. Two variants are evaluated: one trained on all 28 features and one on the top 20 features selected by Random Forest importance.

---

## Contents

| File | Description |
|------|-------------|
| `step5_svm.ipynb` | Full pipeline: feature extraction, selection, SVM training, CV, benchmark |
| `svm_feature_importance.png/.pdf` | Random Forest feature importance ranking (top 20, averaged across 5 folds) |
| `svm_cv_pr_roc_all.png/.pdf` | PR and ROC curves from 5-fold cross-validation (all features) |
| `svm_benchmark_confusion.png/.pdf` | Side-by-side benchmark confusion matrices: all features vs selected features |

---

## Pipeline

### 1 — Feature extraction
28 biochemical features are computed from each protein's N-terminal region. All features target the region where a signal peptide would appear if present.

| Feature group | Features | Region |
|---|---|---|
| AA composition | Frequency of each of 20 amino acids (`comp_A` … `comp_Y`) | First 20 aa |
| Hydrophobicity | `max_hydrophobicity`, `avg_hydrophobicity` (Kyte-Doolittle, window=5) | First 40 aa |
| TM propensity | `max_tm_propensity`, `avg_tm_propensity` (window=5) | First 40 aa |
| Alpha-helix propensity | `max_alpha_propensity`, `avg_alpha_propensity` (window=5) | First 40 aa |
| Charge | `pos_max_charge` (max K/R abundance), `max_charge_abundance` (normalised) | First 40 aa |

### 2 — Feature selection
A Random Forest (200 trees, `random_state=42`) is trained on each of the 5 training folds independently. Feature importances are averaged across folds to avoid data leakage. The top 20 features by mean importance are selected for the reduced model.

Top 5 features by importance: `max_tm_propensity`, `max_hydrophobicity`, `avg_hydrophobicity`, `avg_tm_propensity`, `comp_L` — consistent with the hydrophobic core defining signal peptides.

### 3 — SVM training
An RBF-kernel SVM is trained with nested grid search over C and γ, with MCC as the optimisation metric. The scaler is fit on training folds only (no leakage).

| Parameter | Grid |
|-----------|------|
| Kernel | RBF |
| C | 0.1, 1, 10 |
| γ | `scale`, 0.01, 0.001 |
| Optimisation metric | MCC |

### 4 — 5-fold cross-validation
Both models (all features and selected features) are evaluated with 5-fold CV using the `fold` column from `training_with_folds.tsv`. Per-fold best hyperparameters are recorded.

### 5 — Blind benchmark evaluation
Final models are retrained on the full training set using the most common best hyperparameters across CV folds. The scaler is refit on all training data. Benchmark sequences are never seen during training or hyperparameter selection.

---

## Results

### 5-Fold Cross-Validation — All Features

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.985 |
| PR-AUC | 0.911 |
| F1 | 0.877 |

### Blind Benchmark

| | Predicted SP− | Predicted SP+ |
|---|---|---|
| **All features (28)** | TN=1,759 / FP=28 | FN=29 / TP=190 |
| **Selected features (20)** | TN=1,756 / FP=31 | FN=25 / TP=194 |

Feature selection retains performance while reducing dimensionality by 29%: the selected model gains 4 true positives at the cost of 3 additional false positives.

---

## Comparison with Von Heijne Baseline

| Metric | Von Heijne | SVM (all) | SVM (selected) |
|--------|-----------|-----------|----------------|
| ROC-AUC (CV) | 0.954 | 0.985 | — |
| PR-AUC (CV) | 0.782 | 0.911 | — |
| F1 (CV) | 0.708 | 0.877 | — |
| TP (benchmark) | 158 | 190 | 194 |
| FP (benchmark) | 96 | 28 | 31 |

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
