# Signal Peptide Prediction — LB2 Project · Group 7

A reproducible machine learning pipeline for **eukaryotic signal peptide (SP) prediction**, built from scratch using UniProtKB data. The project progresses from a rule-based statistical baseline to a deep learning model, with full cross-validation and blind benchmark evaluation at every step.

> **Course:** Laboratory of Bioinformatics 2 (LB2) · MSc Bioinformatics · University of Bologna  
> **Group 7**

---

## What This Project Does

Signal peptides are short N-terminal sequences that direct proteins into the secretory pathway. Predicting their presence — and their cleavage site — is a fundamental problem in proteomics and drug target discovery.

This pipeline:
1. Collects a high-confidence labeled dataset from UniProtKB (Swiss-Prot)
2. Removes sequence redundancy using MMseqs2 clustering
3. Performs exploratory analysis to validate biological coherence
4. Trains and evaluates three classifiers of increasing complexity:
   - **Von Heijne** — position-specific weight matrix (PSWM) baseline
   - **SVM** — biochemical features + Random Forest selection
   - **CNN + LSTM** — ESM-2 protein language model embeddings

---

## Repository Structure

```
.
├── 1- Data_Collection/        # Step 1 — UniProtKB retrieval and filtering
├── 2- Data_Preparation/       # Step 2 — MMseqs2 clustering, splits, CV folds
├── 3- Data_analysis/          # Step 3 — Exploratory analysis and visualizations
├── 4- vonHeijne_method/       # Step 4 — PSWM baseline classifier
├── 5- SVM-SPSelection/        # Step 5 — SVM with feature selection
└── 6- Deep_learning/          # Step 6 — CNN-LSTM on ESM-2 embeddings
```

Each folder contains its own `README.md` with detailed documentation, a Jupyter notebook, and all outputs (figures, TSVs, saved models).

---

## Folder Guide

### [`1- Data_Collection/`](./1-%20Data_Collection/README.md)
**Notebook:** `step1_data_collection.ipynb`

Retrieves eukaryotic proteins from UniProtKB via REST API and applies strict experimental evidence filters to produce two labeled sets.

| Set | Criteria | Final count |
|-----|----------|-------------|
| Positive (SP+) | Swiss-Prot, PE1, experimentally confirmed SP, cleavage site known, SP ≥ 14 aa | 2,932 |
| Negative (SP−) | Swiss-Prot, PE1, no SP annotation, localized to cytosol/nucleus/mitochondrion/plastid/peroxisome/membrane | 20,615 |

**Key outputs:** `positive.fasta`, `negative.fasta`, `positive.tsv`, `negative.tsv`

---

### [`2- Data_Preparation/`](./2-%20Data_Preparation/README.md)
**Notebook:** `step2_data_preparation.ipynb`

Removes redundant sequences and constructs train/benchmark splits with cross-validation fold assignments.

| Step | Tool/method | Detail |
|------|-------------|--------|
| Redundancy removal | MMseqs2 `easy-cluster` | 30% identity, 40% coverage, connected-component mode |
| Train/benchmark split | Stratified 80/20 | Per-class shuffle, `RANDOM_SEED=42` |
| CV fold assignment | Stratified 5-fold | `numpy.array_split`, per-class |

| Set | Positive | Negative | Total |
|-----|----------|----------|-------|
| After clustering | 1,093 | 8,934 | 10,027 |
| Training (80%) | ~874 | ~7,147 | 8,021 |
| Benchmark (20%) | ~219 | ~1,787 | 2,006 |

**Key outputs:** `training_with_folds.tsv`, `benchmarking_set.tsv`, `filtered_positive.tsv`, `filtered_negative.tsv`

---

### [`3- Data_analysis/`](./3-%20Data_analysis/README.md)
**Notebook:** `step3_data_analysis.ipynb`

Exploratory analysis performed on the full dataset (train + benchmark) before any model is trained.

| Figure | What it shows |
|--------|---------------|
| `01_protein_length` | SP+ proteins are shorter (median ~300 aa) than SP− (median ~450 aa) |
| `02_sp_length` | SP lengths tightly distributed around mean=22.9 aa, range 14–65 aa |
| `03_aa_composition` | SP regions are enriched in Leu/Ala and depleted in charged residues vs SwissProt background |
| `04_kingdom_distribution` | Both sets dominated by Metazoa; different kingdom proportions noted as potential bias |
| `05_cleavage_site_logo` | Strong Ala conservation at −1 and −3 confirms the von Heijne −1/−3 rule |

All figures are exported as both PNG and PDF inside `3- Data_analysis/`.

---

### [`4- vonHeijne_method/`](./4-%20vonHeijne_method/README.md)
**Notebook:** `step4_von_heijne.ipynb`

Classical PSWM-based classifier. Serves as an interpretable rule-based baseline.

- **Window:** 15 positions (−13 to +2 relative to cleavage site)
- **Scoring:** log-odds vs SwissProt background with pseudocount=1.0
- **Inference:** sliding window over N-terminal positions 15–100, maximum score

| Metric | 5-Fold CV |
|--------|-----------|
| ROC-AUC | 0.954 |
| PR-AUC | 0.782 |
| F1 | 0.708 |

Benchmark confusion matrix: TP=158, FP=96, TN=1691, FN=61

---

### [`5- SVM-SPSelection/`](./5-%20SVM-SPSelection/README.md)
**Notebook:** `step5_svm.ipynb`

SVM classifier on 28 biochemical features extracted from each protein's N-terminal region, with feature selection via Random Forest importance.

- **Features:** AA composition (first 20 aa), hydrophobicity, TM propensity, alpha-helix propensity, charge features (first 40 aa)
- **Selection:** top 20 features by mean Random Forest importance across 5 CV folds
- **SVM:** RBF kernel, grid search over C ∈ {0.1, 1, 10} and γ ∈ {scale, 0.01, 0.001}, optimising MCC

Top features by importance: `max_tm_propensity`, `max_hydrophobicity`, `avg_hydrophobicity`, `avg_tm_propensity`, `comp_L`

| Metric | 5-Fold CV (all 28) | Benchmark (all 28) | Benchmark (top 20) |
|--------|--------------------|--------------------|---------------------|
| ROC-AUC | 0.985 | — | — |
| PR-AUC | 0.911 | — | — |
| F1 | 0.877 | — | — |
| TP | — | 190 | 194 |
| FP | — | 28 | 31 |

---

### [`6- Deep_learning/`](./6-%20Deep_learning/README.md)
**Notebook:** `step6_deep_learning.ipynb`

CNN-LSTM model trained on ESM-2 protein language model embeddings. Best-performing method in the project.

**Architecture:**
- Input: ESM-2 (`esm2_t12_35M_UR50D`, dim=480) embeddings of N-terminal 150 aa
- 3 × Conv1d blocks (64/128/128 filters, kernels 3/5/3) + BatchNorm + MaxPool
- 2-layer bidirectional LSTM (hidden=128)
- Classifier head with Dropout(0.3)

**Training:** Adam lr=1e-3, BCEWithLogitsLoss with class weights (pos_weight≈8.2), ReduceLROnPlateau, early stopping on val MCC (patience=5), gradient clipping (max norm=1.0)

| Metric | 5-Fold CV (mean ± std) | Benchmark |
|--------|------------------------|-----------|
| Precision | 0.971 ± 0.015 | 0.943 |
| Recall | 0.982 ± 0.013 | 0.973 |
| F1 | 0.976 ± 0.007 | 0.957 |
| MCC | 0.973 ± 0.007 | 0.952 |
| PR-AUC | 0.978 ± 0.017 | 0.979 |
| ROC-AUC | 0.997 ± 0.002 | 0.998 |

Benchmark confusion matrix: TP=214, FP=13, TN=1793, FN=6

**Saved model:** `deep_learning/cnn_signal_peptide_model.pt`

---

## Full Model Comparison (Blind Benchmark, n=2,006)

| Model | Precision | Recall | F1 | MCC | PR-AUC | ROC-AUC |
|-------|-----------|--------|----|-----|--------|---------|
| Von Heijne (PSWM) | 0.62 | 0.72 | 0.67 | 0.64 | 0.782 | 0.954 |
| SVM (20 features) | 0.86 | 0.89 | 0.87 | 0.84 | 0.911 | 0.985 |
| **CNN-LSTM (ESM-2)** | **0.943** | **0.973** | **0.957** | **0.952** | **0.979** | **0.998** |

Each method was trained on identical data splits and evaluated on the same held-out benchmark set, enabling direct comparison.

---

## How to Reproduce

All notebooks are designed to run in **Google Colab**. Follow the steps in order:

1. Run `1- Data_Collection/DataCollection.ipynb` → produces `positive.fasta`, `negative.fasta`, `positive.tsv`, `negative.tsv`
2. Upload outputs to `2- Data_Preparation/step2_data_preparation.ipynb` → produces training and benchmark TSVs
3. Upload TSVs + FASTA to subsequent notebooks (steps 3–6), each of which documents its required inputs

Each notebook installs its own dependencies via `pip` and `apt-get`. Required uploads are listed in the **Input Files** section of each folder's `README.md`.

> **Reproducibility:** All random operations use `RANDOM_SEED = 42`. Do not change this value across any step.

---

## Dependencies (summary)

| Tool | Used in |
|------|---------|
| `requests` | data_collection |
| `mmseqs2` | data_preparation |
| `biopython`, `pandas`, `numpy` | all steps |
| `matplotlib`, `seaborn`, `logomaker` | data_analysis |
| `scikit-learn` | von_heijne, SVM, deep_learning |
| `torch`, `fair-esm` | deep_learning |

Full dependency lists are in each folder's `README.md`.

---

## Data Source

- **UniProtKB / Swiss-Prot REST API:** <https://rest.uniprot.org>
- **Swiss-Prot release statistics (ExPASy):** <https://web.expasy.org/docs/relnotes/relstat.html>
- **ESM-2 repository (Meta AI):** <https://github.com/facebookresearch/esm>
