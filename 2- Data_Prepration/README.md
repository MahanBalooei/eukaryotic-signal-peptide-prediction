# Data Preparation

This folder contains the pipeline that takes raw UniProtKB sequences from the data collection step and produces clean, non-redundant, labeled datasets ready for model training and final evaluation.

---

## Contents

| File | Description |
|------|-------------|
| `step2_data_preparation.ipynb` | Full pipeline: clustering, filtering, labeling, splitting, fold assignment |
| `filtered_positive.tsv` | Post-clustering positive sequences (1,093 entries) |
| `filtered_negative.tsv` | Post-clustering negative sequences (8,934 entries) |
| `training_with_folds.tsv` | 80% training split with 5-fold CV labels (8,021 entries) |
| `benchmarking_set.tsv` | 20% held-out benchmark split (2,006 entries) |

---

## Pipeline Overview

### Step 1 — Redundancy removal (MMseqs2)
Positive and negative FASTA files are independently clustered using MMseqs2 `easy-cluster`. One representative sequence is kept per cluster.

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `--min-seq-id` | 0.3 | Minimum 30% sequence identity |
| `-c` | 0.4 | Minimum 40% coverage |
| `--cov-mode` | 0 | Coverage over both query and target |
| `--cluster-mode` | 1 | Connected-component clustering |

### Step 2 — TSV filtering
TSV metadata rows are filtered to retain only the accessions selected as cluster representatives. Consistency between FASTA and TSV is enforced with assertions.

### Step 3 — Labeling
Binary labels are added to the merged dataset: `1` = signal peptide present, `0` = signal peptide absent.

### Step 4 — Stratified 80/20 split
The dataset is split into training (80%) and benchmark (20%) sets **within each class separately**, preserving the positive/negative ratio in both halves. The benchmark set is held out completely and used only once at final evaluation.

### Step 5 — 5-fold cross-validation assignment
Each training sequence is assigned a fold number (0–4), stratified by label. In each CV round, fold `k` serves as the validation set; the remaining four folds are used for training. Fold assignment uses `numpy.array_split`, which distributes remainder rows evenly across folds.

> **Reproducibility:** All shuffles and splits use `RANDOM_SEED = 42`. Do not change this value.

---

## Output Format

All output TSV files share a common base schema, with additional columns depending on the file:

| Column | Type | Description |
|--------|------|-------------|
| `Accession` | str | UniProt accession |
| `Organism` | str | Source organism |
| `Kingdom` | str | Metazoa / Viridiplantae / Fungi / Other |
| `Sequence length` | int | Full sequence length in residues |
| `SP cleavage` | int / NaN | Cleavage site position (positive only) |
| `N-term transmembrane` | bool | N-terminal TM flag (negative only) |
| `label` | int | `1` = SP-positive, `0` = SP-negative |
| `fold` | int | CV fold (0–4); present in `training_with_folds.tsv` only |

---

## Dataset Statistics

| Step | Positive | Negative | Total |
|------|----------|----------|-------|
| Raw (from data collection) | 2,932 | 20,615 | 23,547 |
| After MMseqs2 clustering | 1,093 | 8,934 | 10,027 |
| Training set (80%) | ~874 | ~7,147 | 8,021 |
| Benchmark set (20%) | ~219 | ~1,787 | 2,006 |

Class imbalance ratio: ~8 negatives per positive.

---

## Dependencies

- Python 3.x
- `mmseqs2` (installed via `apt-get` in Colab)
- `biopython`
- `pandas`
- `numpy`

Run `step2_data_preparation.ipynb` in Google Colab. Upload `positive.fasta`, `negative.fasta`, `positive.tsv`, and `negative.tsv` from the `data_collection` folder before executing.
