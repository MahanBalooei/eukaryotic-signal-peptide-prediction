# Von Heijne Signal Peptide Detection Model
## Overview
This repository implements the von Heijne method for detecting signal peptides (SPs) in protein sequences, as part of Practical Session III. The model uses a position-specific scoring matrix (PSSM) based on log-odds ratios to predict SP cleavage sites. Key features include:
- Cleavage-site context: 15 positions spanning -14 to +1 relative to the cleavage site (last SP residue at -1, first mature residue at +1).
- Pseudocounts: Additive smoothing with a pseudocount of 1 for frequency estimation.
- Background model: Swiss-Prot amino acid frequencies for log-odds computation.
- Threshold selection: Cross-validated using precision-recall (PR) curves across 5-fold CV.
- Evaluation: Cross-validation with PR and ROC curves, plus F1-score computation.

The implementation fetches protein sequences from UniProt, extracts cleavage contexts from a provided dataset, builds the model, and evaluates performance. A heatmap visualizes the learned log-odds weights.
Data source: A TSV file (training_with_folds.tsv) with columns including Accession, label (1 for SP-positive), SP cleavage (cleavage position), and fold (for CV splits).

## Key libraries
pandas, numpy, requests, biopython, scikit-learn, matplotlib + Python 3.8+
<pre>
<code class="language-bash">
pip install pandas numpy requests biopython scikit-learn matplotlib
</code>
</pre>
## Usage
1- Prepare data: Place training_with_folds.tsv in the root directory. This file should contain ~1,000 samples (e.g., 873 positives) with UniProt accessions, labels, cleavage sites, and fold assignments./
2- Run cross-validation (main evaluation script):/
