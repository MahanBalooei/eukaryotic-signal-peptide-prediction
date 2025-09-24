import pandas as pd
import numpy as np

np.random.seed(42)
df_train = pd.read_csv('training_set.tsv', sep='\t')

# Separate pos and neg
df_pos = df_train[df_train['label'] == 1]
df_neg = df_train[df_train['label'] == 0]

# Shuffle
pos_indices = np.random.permutation(len(df_pos))
neg_indices = np.random.permutation(len(df_neg))

fold_size_pos = len(df_pos) // 5
fold_size_neg = len(df_neg) // 5

df_train['fold'] = -1

for fold in range(5):
    start_pos = fold * fold_size_pos
    end_pos = start_pos + fold_size_pos if fold < 4 else len(df_pos)
    pos_fold_idx = df_pos.iloc[pos_indices[start_pos:end_pos]].index
    
    start_neg = fold * fold_size_neg
    end_neg = start_neg + fold_size_neg if fold < 4 else len(df_neg)
    neg_fold_idx = df_neg.iloc[neg_indices[start_neg:end_neg]].index
    
    df_train.loc[pos_fold_idx, 'fold'] = fold
    df_train.loc[neg_fold_idx, 'fold'] = fold

# Handle remainders if not divisible by 5 (distribute to earlier folds)
# ...

df_train.to_csv('training_with_folds.tsv', sep='\t', index=False)