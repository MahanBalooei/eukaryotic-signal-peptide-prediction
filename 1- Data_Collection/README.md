# Step 1 — Data Collection from UniProt

**LB2 Project · Group 7 · Signal Peptide Prediction**

This folder contains all scripts and outputs for building the high-quality labeled dataset used in signal peptide (SP) prediction. Sequences are retrieved programmatically from the UniProt REST API and filtered to produce two clean, high-confidence sets: positive (SP-containing) and negative (SP-absent).

---

## Contents

| File                        | Description |
|-----------------------------|-------------|
| `step1_data_collection-2.ipynb` | End-to-end pipeline: UniProt querying, JSON parsing, filtering, and export to TSV + FASTA |
| `positive.tsv`              | Metadata for SP-positive sequences (2,932 entries) |
| `negative.tsv`              | Metadata for SP-negative sequences (20,615 entries) |
| `positive.fasta`            | SP-positive sequences in FASTA format |
| `negative.fasta`            | SP-negative sequences in FASTA format |

---

## Pipeline Overview

1. **Query UniProt REST API** — Structured search URLs with all filters applied at query time; pagination handled automatically with retry logic (`requests` + `Retry` adapter).
2. **Parse JSON responses** — Extract accession, organism, kingdom (Metazoa / Viridiplantae / Fungi / Other), sequence length, and SP-specific metadata.
3. **Filter entries** — Per-entry filter functions enforce strict quality criteria.
4. **Export** — Valid entries are written simultaneously to TSV (metadata) and FASTA (sequences).

---

## Filtering Criteria

### Positive set (SP-present)
- Reviewed (Swiss-Prot) entries only
- Eukaryota (`taxonomy_id:2759`)
- Full-length proteins (no fragments)
- Sequence length ≥ 40 residues
- Protein existence at protein level (PE1)
- Experimentally confirmed signal peptide (`ft_signal_exp:*`)
- SP cleavage site confirmed; mature SP length > 13 residues

### Negative set (SP-absent)
- Reviewed (Swiss-Prot) entries only
- Eukaryota (`taxonomy_id:2759`)
- Full-length proteins (no fragments)
- Sequence length ≥ 40 residues
- No signal peptide annotation of any kind (`NOT ft_signal:*`)
- Experimentally confirmed localization to cytosol, nucleus, mitochondrion, plastid, peroxisome, or cell membrane

---

## Output Format

**TSV columns:**

| File            | Columns |
|-----------------|---------|
| `positive.tsv`  | `Accession`, `Organism`, `Kingdom`, `Sequence length`, `SP cleavage` |
| `negative.tsv`  | `Accession`, `Organism`, `Kingdom`, `Sequence length`, `N-term transmembrane` |

**FASTA headers:** Standard UniProt accession format (e.g. `>O00300`).

---

## Dataset Statistics (as of latest run)

| Set                  | Total Retrieved | After Filtering |
|----------------------|-----------------|-----------------|
| Positive (SP+)       | 2,949           | **2,932**       |
| Negative (SP−)       | 20,615          | **20,615**      |

**Note:** UniProt data can change daily. These numbers exactly match the run in `step1_data_collection-2.ipynb`.

---

## How to Run

Open `step1_data_collection-2.ipynb` in Google Colab (or any Jupyter environment with internet access). All files (`positive.tsv`, `negative.tsv`, `positive.fasta`, `negative.fasta`) will be generated automatically.

**Next step:** Run `data_preparation/step2_data_preparation.ipynb` for MMseqs2 clustering and 80/20 train/benchmark split.

---

**Dependencies**
- Python 3.x
- `requests`
- `pandas`

Ready for the rest of the pipeline!