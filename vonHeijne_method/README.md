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
### 1- Prepare data: 
Place training_with_folds.tsv in the root directory. This file should contain ~1,000 samples (e.g., 873 positives) with UniProt accessions, labels, cleavage sites, and fold assignments.

### 2- Run cross-validation (main evaluation script):
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


<img width="600" height="400" alt="cv_pr_curve" src="https://github.com/user-attachments/assets/90a15570-494d-4eef-bfbe-078764d55aa6" />
<img width="600" height="400" alt="cv_roc_curve" src="https://github.com/user-attachments/assets/cb423f6d-9452-41ba-8b0e-c7ea36165c9c" />



### 3- Generate weight heatmap (visualize full model from all positives):
<pre>
<code class="language-bash">
python Heatmap.py
</code>
</pre>
<img width="800" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/5712b4d0-9808-41af-86a8-f5573517ee4b" />


- Builds PSSM from all positive examples.
- Saves: HM.png

## Model Details
### Von Heijne PSSM Construction
- Extract 15-mer contexts around annotated cleavage sites from positive examples.
- Compute position-specific amino acid frequencies with pseudocount=1.
- Log-odds: (\log\left(\frac{f_{pos,aa}}{b_{aa}}\right)), where (f_{pos,aa}) is the frequency and (b_{aa}) is the Swiss-Prot background.
- Score a potential cleavage at position (k): Sum of log-odds for the context window.
- Max score across possible sites (15 ≤ k ≤ 100) is the protein's SP score.

### Thresholding
- Per-fold: Optimize threshold on PR curve to maximize F1-score.
- Overall: Use average threshold for final predictions.
```
Fold 0: Trained on 699, Best thresh=6.195, F1=0.719  
Fold 1: Trained on 699, Best thresh=6.495, F1=0.714  
Fold 2: Trained on 699, Best thresh=6.809, F1=0.698  
Fold 3: Trained on 699, Best thresh=6.461, F1=0.734  
Fold 4: Trained on 696, Best thresh=6.325, F1=0.768  
Average threshold: 6.457
```

## Summary
<table align="center">
  <thead>
    <tr>
      <th>Metric</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Average threshold</strong></td>
      <td>6.457</td>
    </tr>
    <tr>
      <td><strong>Accuracy</strong></td>
      <td>0.936</td>
    </tr>
    <tr>
      <td><strong>Recall</strong></td>
      <td>0.746</td>
    </tr>
    <tr>
      <td><strong>Precision</strong></td>
      <td>0.688</td>
    </tr>
    <tr>
      <td><strong>MCC</strong></td>
      <td>0.680</td>
    </tr>
    <tr>
      <td><strong>Overall CV F1</strong></td>
      <td>0.716</td>
    </tr>
  </tbody>
</table>

