import pandas as pd
import numpy as np

# Set seed for reproducibility (must match Step 6)
np.random.seed(42)

# Load filtered positive and negative (these should still exist from Step 5)
df_pos_all = pd.read_csv('filtered_positive.tsv', sep='\t')
df_neg_all = pd.read_csv('filtered_negative.tsv', sep='\t')

# Select 20% for benchmarking (reverse of Step 6: 20% bench, 80% train)
bench_pos_idx = np.random.choice(df_pos_all.index, size=int(0.2 * len(df_pos_all)), replace=False)
df_bench_pos = df_pos_all.loc[bench_pos_idx]
df_bench_pos['label'] = 1  # Positive label

bench_neg_idx = np.random.choice(df_neg_all.index, size=int(0.2 * len(df_neg_all)), replace=False)
df_bench_neg = df_neg_all.loc[bench_neg_idx]
df_bench_neg['label'] = 0  # Negative label

# Combine into test (benchmarking) set
df_test = pd.concat([df_bench_pos, df_bench_neg])
df_test.to_csv('test_set_labeled.tsv', sep='\t', index=False)

print(f"Test set created: {len(df_test)} sequences (Pos: {len(df_bench_pos)}, Neg: {len(df_bench_neg)})")
print("Saved to 'test_set_labeled.tsv'")