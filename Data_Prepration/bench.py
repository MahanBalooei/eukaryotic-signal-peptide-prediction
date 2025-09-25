import pandas as pd

df_bench = pd.read_csv('benchmarking_set.tsv', sep='\t')
print("Columns in benchmarking_set.tsv:", df_bench.columns.tolist())
print("\nFirst few rows:")
print(df_bench.head())