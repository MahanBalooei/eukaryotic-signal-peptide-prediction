# Data Analysis

This folder contains the exploratory data analysis (EDA) performed on the full labeled dataset (training + benchmark combined) before any model is trained. The goal is to confirm biological coherence, detect taxonomic or compositional biases, and identify sequence features informative for classification.

---

## Contents

| File | Description |
|------|-------------|
| `step3_data_analysis.ipynb` | Full EDA pipeline with inline commentary |
| `01_protein_length.png/.pdf` | Protein length distribution — SP+ vs SP− |
| `02_sp_length.png/.pdf` | Signal peptide length distribution (SP+ only) |
| `03_aa_composition.png/.pdf` | Amino acid composition vs SwissProt background |
| `04_kingdom_distribution.png/.pdf` | Taxonomic kingdom distribution — SP+ vs SP− |
| `05_cleavage_site_logo.png/.pdf` | Sequence logo around the cleavage site (positions −13 to +2) |

---

## Analyses

### 1 — Protein length distribution
Compares full-length protein sizes between SP+ (n=1,093) and SP− (n=8,934) sets using a density histogram (clipped at 2,000 aa) and a boxplot. SP+ proteins are shorter on average (median ~300 aa) than SP− proteins (median ~450 aa), consistent with the expectation that cytosolic/nuclear proteins tend to be larger.

### 2 — Signal peptide length distribution
Examines the cleavage position (= SP length) across all SP+ sequences. SP lengths are tightly distributed between 14 and 40 aa, with a mean of 22.9 aa and a median of 22 aa, consistent with the canonical hydrophobic core length required for translocon insertion.

### 3 — Amino acid composition vs SwissProt background
Computes per-residue frequency in two regions: the SP region of SP+ sequences and the N-terminal 30 aa of SP− sequences. Both are compared against the SwissProt proteome-wide background (ExPASy release statistics). The SP region is markedly enriched in hydrophobic residues (Leu, Ala) and depleted in charged and polar residues, reflecting the hydrophobic core characteristic of signal peptides.

### 4 — Kingdom distribution
Counts sequences by taxonomic kingdom (Metazoa, Viridiplantae, Fungi, Other) for both classes. Both sets are dominated by Metazoa (SP+: 79.3%, SP−: 52.6%), with Fungi and Viridiplantae as secondary kingdoms. The different proportions between classes are noted as a potential source of taxonomic bias in model evaluation.

### 5 — Cleavage site sequence logo
Extracts a 15-residue window (positions −13 to +2 relative to the cleavage site) from all SP+ sequences with valid FASTA entries. A position frequency matrix is built, converted to an information-content matrix using `logomaker`, and displayed as a sequence logo. Strong conservation of Ala at position −1 and Ala/Gly at position −3 confirms the **von Heijne −1/−3 rule** for signal peptidase recognition, validating annotation quality.

---

## Methods

| Library | Usage |
|---------|-------|
| `pandas`, `numpy` | Data loading and manipulation |
| `matplotlib`, `seaborn` | Histograms, boxplots, bar charts |
| `logomaker` | Sequence logo from information-content matrix |
| `biopython` (`SeqIO`) | FASTA parsing for sequence extraction |

All figures are saved in both PNG (screen) and PDF (publication) formats to `figures/`.

---

## Input Files

Upload the following files to Colab before running the notebook:

- `training_with_folds.tsv` — from `data_preparation/`
- `benchmarking_set.tsv` — from `data_preparation/`
- `positive.fasta` — from `data_collection/`
- `negative.fasta` — from `data_collection/`

---

## Dependencies

```
pip install biopython pandas numpy matplotlib seaborn logomaker
```
