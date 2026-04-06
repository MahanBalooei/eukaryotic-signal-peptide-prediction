# Data Collection

This folder contains the scripts and outputs for building the labeled dataset used in signal peptide (SP) prediction. Sequences are retrieved programmatically from UniProt and filtered to produce two balanced, high-confidence sets: positive (SP-containing) and negative (SP-absent).

---

## Contents

| File | Description |
|------|-------------|
| `DataCollection.ipynb` | End-to-end pipeline: UniProt querying, JSON parsing, filtering, and export |
| `positive.tsv` | Metadata for SP-positive sequences (2,932 entries) |
| `negative.tsv` | Metadata for SP-negative sequences (20,615 entries) |
| `positive.fasta` | SP-positive sequences in FASTA format |
| `negative.fasta` | SP-negative sequences in FASTA format |

---

## Pipeline Overview

1. **Query UniProt REST API** — Structured URLs with filters applied at query time; pagination handled with retry logic (`requests` + `Retry` adapter).
2. **Parse JSON responses** — Each entry is parsed to extract accession, organism, taxonomic kingdom (Metazoa / Viridiplantae / Fungi / Other), sequence length, and SP-specific metadata.
3. **Filter entries** — Per-entry filter functions (`filter_entry_positive`, `filter_entry_negative`) enforce quality criteria (see below).
4. **Export** — Passing entries are written to TSV (metadata) and FASTA (sequence) files simultaneously.

---

## Filtering Criteria

### Positive set (SP-present)
- Reviewed (Swiss-Prot) entries only
- Eukaryota (`taxonomy_id:2759`)
- Full-length proteins (no fragments)
- Sequence length ≥ 40 residues
- Protein existence at protein level (PE1)
- Experimentally confirmed signal peptide (`ft_signal_exp`)
- SP cleavage site confirmed; mature SP length > 13 residues

### Negative set (SP-absent)
- Reviewed (Swiss-Prot) entries only
- Eukaryota (`taxonomy_id:2759`)
- Full-length proteins (no fragments)
- Sequence length ≥ 40 residues
- No signal peptide annotation of any kind (`NOT ft_signal`)
- Experimentally confirmed localization to: cytosol, nucleus, mitochondrion, plastid, peroxisome, or cell membrane

---

## Output Format

**TSV columns:**

| File | Columns |
|------|---------|
| `positive.tsv` | `Accession`, `Organism`, `Kingdom`, `Sequence length`, `SP cleavage` |
| `negative.tsv` | `Accession`, `Organism`, `Kingdom`, `Sequence length`, `N-term transmembrane` |

**FASTA headers:** Standard UniProt accession format (e.g., `>O00300`).

---

## Dataset Statistics

| Set | Retrieved | After filtering |
|-----|-----------|-----------------|
| Positive | 2,949 | 2,932 |
| Negative | 20,615 | 20,615 |

---

## Dependencies

- Python 3.x
- `requests`
- `pandas`

Run `DataCollection.ipynb` in Google Colab or any Jupyter environment with internet access.
