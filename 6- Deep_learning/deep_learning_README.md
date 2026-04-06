# Deep Learning — CNN Classifier

This folder implements a 1D Convolutional Neural Network (CNN) with an LSTM layer on top of ESM-2 protein language model embeddings for signal peptide classification. It is the highest-performing method in the project.

---

## Contents

| File | Description |
|------|-------------|
| `step6_deep_learning.ipynb` | Full pipeline: ESM-2 embedding, CNN-LSTM training, CV, benchmark |
| `cnn_signal_peptide_model.pt` | Saved weights of the final model (PyTorch state dict) |
| `cnn_cv_results.tsv` | Per-fold CV metrics (precision, recall, F1, MCC, PR-AUC, ROC-AUC) |
| `cnn_training_history.tsv` | Per-epoch training/validation loss and MCC for all 5 folds |
| `cnn_model_comparison.tsv` | Side-by-side benchmark comparison: Von Heijne vs SVM vs CNN |
| `cnn_training_curves.png/.pdf` | Validation MCC, training loss, validation loss per epoch across folds |
| `cnn_cv_metrics.png/.pdf` | Per-fold CV metric trajectories |
| `cnn_benchmark_pr_roc.png/.pdf` | PR and ROC curves on the blind benchmark set |
| `cnn_benchmark_confusion.png/.pdf` | Confusion matrix on the blind benchmark set |

---

## Architecture — SignalCNN

Input: ESM-2 embeddings of the N-terminal 150 aa → shape `(B, 150, 480)`

| Layer | Details |
|-------|---------|
| Conv block 1 | Conv1d(480→64, k=3, pad=1) → ReLU → BatchNorm1d → MaxPool1d(2) |
| Conv block 2 | Conv1d(64→128, k=5, pad=2) → ReLU → BatchNorm1d → MaxPool1d(2) |
| Conv block 3 | Conv1d(128→128, k=3, pad=1) → ReLU → BatchNorm1d |
| LSTM | 2-layer bidirectional LSTM (hidden=128) |
| Classifier | Flatten → Dropout(0.3) → Linear(128→64) → ReLU → Dropout(0.3) → Linear(64→1) |
| Output | Single logit → sigmoid for SP probability |

Three convolutional blocks with kernel sizes 3, 5, 3 capture local motifs at increasing scales. The bidirectional LSTM captures long-range sequence dependencies. BatchNorm stabilises training on the imbalanced dataset (~8:1 negative-to-positive ratio).

---

## Pipeline

### 1 — ESM-2 embedding
Each protein's N-terminal 150 residues are encoded using the `esm2_t12_35M_UR50D` model (35M parameters, embedding dim=480). Embeddings are pre-computed once per run and stored in memory. CLS and EOS tokens are removed; sequences shorter than 150 aa are zero-padded.

### 2 — Training setup
- **Loss:** `BCEWithLogitsLoss` with `pos_weight = n_neg / n_pos ≈ 8.2` to compensate for class imbalance
- **Optimizer:** Adam (lr=1e-3)
- **LR scheduler:** ReduceLROnPlateau (factor=0.5, patience=3 epochs on validation loss)
- **Early stopping:** patience=5 epochs tracked on validation MCC; best weights restored
- **Gradient clipping:** max norm=1.0 (required for LSTM stability)

### 3 — 5-fold cross-validation
One model is trained per fold using the `fold` column from `training_with_folds.tsv`. The final model is retrained on the full training set for the average number of epochs across CV early stopping points.

### 4 — Blind benchmark evaluation
The final model is applied to the benchmark set — sequences never seen during training or CV. PR-AUC, ROC-AUC, F1, MCC, and confusion matrix are reported.

---

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| Input window | 150 aa (N-terminal) |
| ESM-2 model | `esm2_t12_35M_UR50D` (dim=480) |
| Batch size | 32 |
| Learning rate | 1e-3 |
| LR scheduler | ReduceLROnPlateau (factor=0.5, patience=3) |
| Early stopping patience | 5 epochs (on val MCC) |
| Dropout | 0.3 |
| Random seed | 42 |

---

## Results

### 5-Fold Cross-Validation (mean ± std)

| Metric | Mean | Std |
|--------|------|-----|
| Precision | 0.971 | 0.015 |
| Recall | 0.982 | 0.013 |
| F1 | 0.976 | 0.007 |
| MCC | 0.973 | 0.007 |
| PR-AUC | 0.978 | 0.017 |
| ROC-AUC | 0.997 | 0.002 |

### Blind Benchmark (n = 2,006)

| | Predicted SP− | Predicted SP+ |
|---|---|---|
| **True SP−** | 1,793 (TN) | 13 (FP) |
| **True SP+** | 6 (FN) | 214 (TP) |

Benchmark F1=0.957, PR-AUC=0.979, ROC-AUC=0.998.

---

## Full Model Comparison (Benchmark Set)

| Model | Precision | Recall | F1 | MCC | PR-AUC | ROC-AUC |
|-------|-----------|--------|----|-----|--------|---------|
| Von Heijne (PSWM) | 0.62 | 0.72 | 0.67 | 0.64 | 0.782 | 0.954 |
| SVM (selected, 20 feat.) | 0.86 | 0.89 | 0.87 | 0.84 | 0.911 | 0.985 |
| **CNN (ESM-2, 150 aa)** | **0.943** | **0.973** | **0.957** | **0.952** | **0.979** | **0.998** |

---

## Loading the Saved Model

```python
import torch
from step6_deep_learning import SignalCNN  # or copy the class definition

model = SignalCNN(input_dim=480, max_len=150)
model.load_state_dict(torch.load('cnn_signal_peptide_model.pt', map_location='cpu'))
model.eval()
```

---

## Input Files

Upload the following to Colab before running:

- `training_with_folds.tsv` — from `data_preparation/`
- `benchmarking_set.tsv` — from `data_preparation/`
- `positive.fasta` — from `data_collection/`
- `negative.fasta` — from `data_collection/`

---

## Dependencies

```
pip install biopython torch fair-esm pandas numpy matplotlib seaborn scikit-learn
```

> **Note:** ESM-2 embedding pre-computation requires a GPU (recommended). On Google Colab, use a T4 GPU runtime.
