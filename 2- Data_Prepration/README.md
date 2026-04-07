# Step 2 — Data Preparation

**LB2 Project · Group 7 · Signal Peptide Prediction**

This folder takes the raw positive and negative datasets from Step 1 and produces clean, non-redundant, labeled datasets ready for model training and final evaluation.

---

## Contents

| File                        | Description |
|-----------------------------|-------------|
| `step2_data_preparation.ipynb` | Full pipeline: MMseqs2 clustering, metadata filtering, labeling, 80/20 split, and 5-fold CV assignment |
| `filtered_positive.tsv`     | Positive cluster representatives with metadata (1,093 entries) |
| `filtered_negative.tsv`     | Negative cluster representatives with metadata (8,934 entries) |
| `training_with_folds.tsv`   | Training set (80 %) with `label` and `fold` columns (8,021 entries) |
| `benchmarking_set.tsv`      | Held-out benchmark set (20 %) with `label` column — **never used during training** (2,006 entries) |

---

## Pipeline Overview

1. **Redundancy removal (MMseqs2)** — Independent clustering of positive and negative sequences (`easy-cluster`).
2. **TSV filtering** — Keep only cluster representatives in the metadata files.
3. **Labeling** — Add binary `label` column (`1` = SP-positive, `0` = SP-negative).
4. **Stratified 80/20 split** — Performed **within each class** to preserve class ratio. Benchmark set is held out completely.
5. **5-fold cross-validation** — Assigned only to the training set, stratified by label.

**Reproducibility:** All random operations use `RANDOM_SEED = 42`.

---

## MMseqs2 Clustering Parameters

| Parameter      | Value | Meaning |
|----------------|-------|---------|
| `--min-seq-id` | 0.3   | Minimum 30 % sequence identity |
| `-c`           | 0.4   | Minimum 40 % coverage |
| `--cov-mode`   | 0     | Coverage over both query and target |
| `--cluster-mode` | 1   | Connected-component clustering |

---

## Output Format

All TSV files share the same base columns plus extra fields:

| Column                | Description |
|-----------------------|-------------|
| `Accession`           | UniProt accession |
| `Organism`            | Source organism |
| `Kingdom`             | Metazoa / Viridiplantae / Fungi / Other |
| `Sequence length`     | Full protein length |
| `SP cleavage`         | Cleavage site (positive only) |
| `N-term transmembrane`| N-terminal TM helix flag (negative only) |
| `label`               | `1` = SP-positive, `0` = SP-negative |
| `fold`                | CV fold (0–4) — only in `training_with_folds.tsv` |

---

## Dataset Statistics

| Step                          | Positive | Negative | Total  |
|-------------------------------|----------|----------|--------|
| Raw (from Step 1)             | 2,932    | 20,615   | 23,547 |
| After MMseqs2 clustering      | **1,093**| **8,934**| 10,027 |
| Training set (80 %)           | 874      | 7,147    | **8,021** |
| Benchmarking set (20 %)       | 219      | 1,787    | **2,006** |

Class imbalance ≈ 8.2 negatives per positive.

---

## How to Run

1. Upload the four files from the **Data Collection** folder:
   - `positive.fasta`, `negative.fasta`
   - `positive.tsv`, `negative.tsv`
2. Run `step2_data_preparation.ipynb` in Google Colab.
3. All output files will be generated automatically.

**Next step:** Proceed to the deep learning notebook (`step6_deep_learning_latest_version_negin.ipynb`).

---

**Dependencies**
- Python 3.x
- `mmseqs2` (installed via `apt-get`)
- `biopython`
- `pandas`, `numpy`

Ready for model training!