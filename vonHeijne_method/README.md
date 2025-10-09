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
1- Prepare data: Place training_with_folds.tsv in the root directory. This file should contain ~1,000 samples (e.g., 873 positives) with UniProt accessions, labels, cleavage sites, and fold assignments.

2- Run cross-validation (main evaluation script):
<pre>
<code class="language-bash">
python codebase.py
</code>
</pre>

- Fetches sequences from UniProt.
- Performs 5-fold cross-validation.
- Builds the von Heijne PSSM per fold (from training positives).
- Predicts scores and selects thresholds via PR curve maximization of F1.
- Outputs console logs (e.g., per-fold F1, average threshold ~0.5-1.0, overall CV F1 ~0.7-0.8).
- Saves plots: cv_pr_curve.png and cv_roc_curve.png.
<img width="800" height="600" alt="cv_pr_curve" src="https://github.com/user-attachments/assets/90a15570-494d-4eef-bfbe-078764d55aa6" />

<img width="800" height="600" alt="cv_roc_curve" src="https://github.com/user-attachments/assets/cb423f6d-9452-41ba-8b0e-c7ea36165c9c" />

3- Generate weight heatmap (visualize full model from all positives):
<pre>
<code class="language-bash">
python Heatmap.py
</code>
</pre>
<img width="3319" height="2363" alt="von_heijne_weights_heatmap" src="https://github.com/user-attachments/assets/d26cbfde-ce14-4e5d-8b70-92f50289ffcf" />


