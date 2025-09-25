# Data Preprocessing and Splitting
This repository contains scripts and instructions for reducing data redundancy, clustering protein sequences, selecting representative sequences, and preparing training and benchmarking datasets with 5-fold cross-validation subsets. The pipeline is designed to process positive and negative protein sequences stored in TSV files, using MMSeqs2 for clustering and Python for data manipulation.
## Objective
The goal of this part is to:
- Reduce data redundancy by clustering positive and negative sequences separately using MMSeqs2.
- Select representative sequences from each cluster.
- Generate new TSV files containing only the representative sequences.
- Split the data into training (80%) and benchmarking (20%) sets, preserving the positive/negative ratio.
- Create 5-fold cross-validation subsets from the training set, maintaining the positive/negative ratio in each subset.
