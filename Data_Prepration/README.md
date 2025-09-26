# Data Preprocessing and Splitting
This repository contains scripts and instructions for reducing data redundancy, clustering protein sequences, selecting representative sequences, and preparing training and benchmarking datasets with 5-fold cross-validation subsets. The pipeline is designed to process positive and negative protein sequences stored in TSV files, using MMSeqs2 for clustering and Python for data manipulation.
## Objective
The goal of this part is to:
- Reduce data redundancy by clustering positive and negative sequences separately using MMSeqs2.
- Select representative sequences from each cluster.
- Generate new TSV files containing only the representative sequences.
- Split the data into training (80%) and benchmarking (20%) sets, preserving the positive/negative ratio.
- Create 5-fold cross-validation subsets from the training set, maintaining the positive/negative ratio in each subset.

## Pipeline Steps
### Cluster Sequences Using MMSeqs2
Positive and negative sequences are clustered separately at 30% sequence identity and 40% coverage using MMSeqs2.
The following MMSeqs2 command is used:
<pre>
<code class="language-bash">
mmseqs easy-cluster input.fa cluster-results tmp \
  --min-seq-id 0.3 \
  -c 0.4 \
  --cov-mode 0 \
  --cluster-mode 1
</code>
</pre>
  
### Outputs per dataset (positive/negative):
- ![file](https://img.shields.io/badge/cluster--results_rep__seq.fasta-orange) : FASTA file with representative sequences (one per cluster).
- ![file](https://img.shields.io/badge/cluster--results_cluster.tsv-orange) : TSV file with two columns:\
Column 1: Sequence ID from the input file.\
Column 2: ID of the representative sequence for the cluster.

Representative sequences are saved as (https://github.com/username/repo/blob/main/LB2_project_Group_7/Data_Prepration/cluster-results1_cluster.tsv) (2,932 sequences) and (https://github.com/username/repo/blob/main/LB2_project_Group_7/Data_Prepration/cluster-results2_cluster.tsv) (20,615 sequences).


