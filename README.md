# Eukaryotic Signal Peptide Prediction: PSWM, SVM and ESM-2 Embeddings

MSc Bioinformatics, University of Bologna. Project for the Laboratory of Bioinformatics 2 course.

This repository compares three ways of predicting whether a eukaryotic protein carries an N-terminal signal peptide: a von Heijne position-specific weight matrix, an SVM on hand-crafted biochemical features, and a CNN-BiLSTM on ESM-2 embeddings. All three are trained on the same training set and tested once on the same held-out benchmark.

The course assigned this as a group project (Group 7), and the repository began in autumn 2025 as shared work with Kimia Kanouni and Negin Nilforoosh. In April 2026 I rebuilt the pipeline on my own. The data preparation, exploratory analysis, all three models, the evaluation and the documentation in this repository are my implementation. The UniProt retrieval functions in the step 1 notebook are kept from the group's original version.

## Results on the held-out benchmark (2,006 proteins, 219 positives)

| Model | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|
| von Heijne PSWM | 0.625 | 0.717 | 0.668 | 0.626 |
| SVM, 28 features | 0.872 | 0.868 | 0.870 | 0.854 |
| CNN-BiLSTM on ESM-2 | 0.951 | 0.973 | 0.962 | 0.957 |

The benchmark has only 219 positives and comes from a single split, so these numbers have no confidence intervals. Read the ranking as clear and the exact values as approximate. The section on limitations below says what else to keep in mind.

## Why signal peptides

Signal peptides are short N-terminal sequences that send a protein into the secretory pathway and are then cleaved off. Knowing whether a protein has one matters when annotating new proteomes, when designing proteins for secretion, and when looking for secreted drug targets.

## How the data were built

**Collection (step 1).** Proteins come from UniProtKB/Swiss-Prot through the REST API, restricted to eukaryotes with protein-level evidence (PE1).

| Set | Criteria | Proteins |
|---|---|---:|
| Positive | Experimentally confirmed signal peptide, known cleavage site, signal peptide of at least 14 residues | 2,932 |
| Negative | No signal peptide annotation, experimentally confirmed location in cytosol, nucleus, mitochondrion, plastid, peroxisome or membrane | 20,615 |

**Redundancy reduction and split (step 2).** Positives and negatives were clustered separately with MMseqs2 `easy-cluster` (30% identity, 40% coverage, connected-component mode), and only one representative per cluster was kept. The 80/20 train/benchmark split was made afterwards, on the representatives, stratified by class. So within each class, no two proteins anywhere in the dataset come from the same cluster, which is what keeps close homologs from sitting on both sides of the split. Clustering was done per class, so similarity between a positive and a negative was not filtered.

| Stage | Positive | Negative | Total |
|---|---:|---:|---:|
| Raw | 2,932 | 20,615 | 23,547 |
| After clustering | 1,093 | 8,934 | 10,027 |
| Training (80%) | 874 | 7,147 | 8,021 |
| Benchmark (20%) | 219 | 1,787 | 2,006 |

The training set carries pre-assigned 5-fold cross-validation labels, and the same folds are used by all three models.

**How the benchmark was protected.** The benchmark was set aside in step 2 and used only for the final evaluation of each model. Every tuning decision was made inside the training set:

- SVM: C and gamma were chosen by cross-validation on the training folds (nested CV for the reported CV scores, plain 5-fold CV for the final model).
- CNN-BiLSTM: early stopping watched the MCC of the validation fold. The final model was then retrained on the whole training set for the median best epoch found in CV, with no access to the benchmark.

## The three models

### von Heijne PSWM (step 4)

A weight matrix over 15 positions around the cleavage site (-13 to +2), scored as log-odds against the Swiss-Prot background with a pseudocount of 1. At prediction time the matrix slides over N-terminal positions 15 to 100 and the best score is kept. It is a weak classifier but an easy one to inspect, and the matrix shows the expected hydrophobic core and the -3/-1 rule, which is a useful check on the dataset.

5-fold CV: ROC-AUC 0.954, PR-AUC 0.782, F1 0.708.
Benchmark: TP 157, FP 94, TN 1,693, FN 62.

### SVM on biochemical features (step 5)

An RBF-kernel SVM on 28 features from the N-terminus: amino acid composition of the first 20 residues, and hydrophobicity, transmembrane propensity, helix propensity and charge over the first 40. A random forest ranks the features. The five most important are maximum and average transmembrane propensity, maximum and average hydrophobicity, and leucine content, which is what you would expect from the hydrophobic core of a signal peptide.

5-fold CV (all 28 features): ROC-AUC 0.986, PR-AUC 0.918, F1 0.868.
Benchmark: TP 190, FP 28 with all 28 features; TP 188, FP 29 with the top 20.

### CNN-BiLSTM on ESM-2 embeddings (step 6)

- Input: per-residue embeddings of the first 150 residues from `esm2_t12_35M_UR50D` (480 dimensions). The language model is frozen; only the classifier is trained.
- Three Conv1d blocks (64, 128, 128 filters; kernels 3, 5, 3) with batch normalisation and max pooling
- Two-layer bidirectional LSTM, hidden size 128
- Classifier head with dropout 0.3
- Adam (lr 1e-3), class-weighted BCE loss (positive weight about 8.2), gradient clipping at 1.0

| Metric | 5-fold CV (mean ± sd) | Benchmark |
|---|---|---:|
| Precision | 0.976 ± 0.014 | 0.951 |
| Recall | 0.974 ± 0.009 | 0.973 |
| F1 | 0.975 ± 0.006 | 0.962 |
| MCC | 0.972 ± 0.007 | 0.957 |
| PR-AUC | 0.980 ± 0.009 | 0.984 |
| ROC-AUC | 0.996 ± 0.001 | 0.998 |

Benchmark: TP 213, FP 11, TN 1,776, FN 6. The trained weights are in `6- Deep_learning/cnn_signal_peptide_model.pt`.

## Limitations

- **The negatives are the easy ones.** They are proteins with a confirmed non-secretory location. Secreted proteins without a signal peptide, and proteins whose N-terminal transmembrane helix looks like one, are the cases that make this problem hard in a real proteome, and the first group is absent here. Expect lower performance on a whole proteome than on this benchmark.
- **The models do not see the same input.** The PSWM uses a 15-residue window, the SVM the first 20 to 40 residues, the CNN the first 150. I did not run an ablation, so I cannot say how much of the CNN's advantage comes from the ESM-2 representation and how much from the longer window or the architecture.
- **One split, one seed.** Everything uses `RANDOM_SEED = 42`. The CV standard deviations give some idea of the variance, but the benchmark figures are single numbers.
- **Small language model.** I used the 35M-parameter ESM-2 to stay within Colab limits. Larger checkpoints were not tested.
- **No comparison with SignalP** or other published predictors on the same benchmark.

## Repository layout

```
1- Data_Collection/     UniProtKB retrieval and filtering
2- Data_Preparation/    MMseqs2 clustering, train/benchmark split, CV folds
3- Data_analysis/       Exploratory analysis and figures
4- vonHeijne_method/    PSWM baseline
5- SVM-SPSelection/     SVM with feature selection
6- Deep_learning/       CNN-BiLSTM on ESM-2 embeddings
```

Each folder has its own README, the notebook, and the outputs it produced (tables, figures, and for step 6 the trained model). The exploratory analysis in step 3 covers protein length, signal peptide length (mean 22.9 residues, range 14 to 65), amino acid composition, taxonomic distribution and the cleavage-site logo.

## Running it

The notebooks were written for Google Colab and are meant to be run in order.

1. Run `1- Data_Collection/step1_data_collection.ipynb`. It writes `positive.fasta`, `negative.fasta`, `positive.tsv` and `negative.tsv`.
2. Upload those four files to `2- Data_Preparation/step2_data_preparation.ipynb`, which writes the training and benchmark tables.
3. Steps 3 to 6 each need the tables and FASTA files from the earlier steps; the README in each folder lists exactly which.

Passing files between notebooks by hand is the weak point of the setup. The outputs of every step are committed, so any single notebook can be run without repeating the ones before it. Step 1 queries the live UniProt API, so re-running it later will return a slightly different dataset as Swiss-Prot is updated; the committed files are the ones behind the numbers above.

Python packages are listed in `requirements.txt`. MMseqs2 is installed separately (`apt-get install mmseqs2` on Colab, or through bioconda). Step 6 needs a GPU to finish in reasonable time.

## Sources

- UniProtKB/Swiss-Prot REST API: <https://www.uniprot.org/help/api>
- ESM-2: Lin et al., Science 2023, <https://github.com/facebookresearch/esm>
- MMseqs2: Steinegger and Söding, Nature Biotechnology 2017
- von Heijne G., Nucleic Acids Research 1986

## Contact

Mahan Balooei, mahan.balooei@studio.unibo.it

## License

MIT. See `LICENSE`.
