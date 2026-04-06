# LB2 Project — Group 7  
**Signal Peptide Prediction**

**Final Deep Learning Model** (Step 6)

---

## 📋 Overview

This folder contains the **complete deep learning pipeline** for signal peptide (SP) prediction developed by **Group 7**.

We built a **hybrid CNN-LSTM model** that uses **ESM-2 protein language model embeddings** (480-dimensional) as input. The model significantly outperforms all previous baselines and competing groups in the project.

**Best Benchmark Performance:**
- **MCC**: **0.9524**
- **F1-score**: 0.9575
- **Precision**: 0.9427
- **Recall**: 0.9727

---

## 📁 Key Files in This Folder

| File | Description |
|------|-------------|
| `step6_deep_learning_latest_version_negin.ipynb` | **Main notebook** – Full ESM-2 + CNN-LSTM pipeline (training, 5-fold CV, final model, benchmark evaluation) |
| `step2_data_preparation.ipynb` | Data preprocessing notebook (MMseqs2 clustering + stratified splits) |
| `training_with_folds.tsv` | Training set (80%) with 5-fold CV labels |
| `benchmarking_set.tsv` | Held-out benchmark set (20%) – used only for final evaluation |
| `filtered_positive.tsv` / `filtered_negative.tsv` | Clustered representative sequences after redundancy removal |
| `cnn_signal_peptide_model.pt` | Trained model weights (PyTorch) |
| `cnn_cv_results.tsv` | 5-fold cross-validation metrics |
| `cnn_model_comparison.tsv` | Comparison with Von Heijne PSWM and SVM baselines |
| `figures/` | Training curves, confusion matrix, PR/ROC curves |

---

## 🧪 Model Architecture

- **Input**: ESM-2 (esm2_t12_35M_UR50D) embeddings → 150 aa N-terminal window (480-dim)
- **Architecture**: 3× Conv1d blocks + 2-layer bidirectional LSTM + classifier head
- **Key features**:
  - Early stopping on validation MCC
  - ReduceLROnPlateau scheduler
  - Class-weighted BCEWithLogitsLoss
  - Gradient clipping for LSTM stability

**Total parameters**: ~876k

---

## 📊 Performance Summary

| Metric     | 5-Fold CV Mean (± std) | Benchmark |
|------------|------------------------|---------|
| MCC        | 0.9728 ± 0.0080        | **0.9524** |
| F1         | 0.9756 ± 0.0072        | 0.9575 |
| Precision  | 0.9699 ± 0.0164        | 0.9427 |
| Recall     | 0.9817 ± 0.0124        | 0.9727 |
| ROC-AUC    | 0.9965 ± 0.0022        | 0.9977 |
| PR-AUC     | 0.9780 ± 0.0163        | 0.9787 |

**Comparison with other groups**:
- Group 3 (best previous): MCC ≈ 0.902
- Our model: **+0.050 MCC improvement**

---

## ▶️ How to Reproduce

1. Open `step6_deep_learning_latest_version_negin.ipynb` in Google Colab
2. Run cells in order (all dependencies are installed inside the notebook)
3. The final model and all result files will be generated automatically

**Note**: The data files (`training_with_folds.tsv`, `benchmarking_set.tsv`, etc.) are already included.

---

## 🛠️ Dependencies

- PyTorch
- fair-esm (for ESM-2)
- BioPython
- pandas, numpy, scikit-learn, matplotlib, seaborn

All packages are installed automatically in the notebook.

---

## 👥 Group 7 Members
*(Add your names here)*

---

**Repository**: [https://github.com/MahanBalooei/LB2_project_Group_7](https://github.com/MahanBalooei/LB2_project_Group_7)

Made with ❤️ for LB2 – Signal Peptide Prediction Project
