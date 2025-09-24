import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# For positive
df_pos = pd.read_csv('filtered_positive.tsv', sep='\t')
train_pos_idx = np.random.choice(df_pos.index, size=int(0.8 * len(df_pos)), replace=False)
df_train_pos = df_pos.loc[train_pos_idx]
df_bench_pos = df_pos.drop(train_pos_idx)

# For negative
df_neg = pd.read_csv('filtered_negative.tsv', sep='\t')
train_neg_idx = np.random.choice(df_neg.index, size=int(0.8 * len(df_neg)), replace=False)
df_train_neg = df_neg.loc[train_neg_idx]
df_bench_neg = df_neg.drop(train_neg_idx)

# Save training (combine pos and neg)
df_train = pd.concat([df_train_pos, df_train_neg])
df_train.to_csv('training_set.tsv', sep='\t', index=False)

# Save benchmarking
df_bench = pd.concat([df_bench_pos, df_bench_neg])
df_bench.to_csv('benchmarking_set.tsv', sep='\t', index=False)

print(f"Training: {len(df_train)} (Pos: {len(df_train_pos)}, Neg: {len(df_train_neg)})")
print(f"Benchmarking: {len(df_bench)} (Pos: {len(df_bench_pos)}, Neg: {len(df_bench_neg)})")
 