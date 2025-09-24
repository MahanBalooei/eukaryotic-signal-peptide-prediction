import pandas as pd

# Load representatives
with open('positive_reps.txt') as f:
    positive_reps = set(line.strip() for line in f)

with open('negative_reps.txt') as f:
    negative_reps = set(line.strip() for line in f)

# Filter positive TSV (no header, so columns are 0, 1, etc.)
df_pos = pd.read_csv('positive.tsv', sep='\t')
print (len(df_pos))
df_pos_filtered = df_pos[df_pos["Accession"].isin(positive_reps)]  # Assume column 0 is the ID
df_pos_filtered.to_csv('filtered_positive.tsv', sep='\t', index=False)  # No header in output
print(f"Filtered positive: {len(df_pos_filtered)} rows")

# Filter negative TSV
df_neg = pd.read_csv('negative.tsv', sep='\t')
df_neg_filtered = df_neg[df_neg["Accession"].isin(negative_reps)]  # Assume column 0 is the ID
df_neg_filtered.to_csv('filtered_negative.tsv', sep='\t', index=False)
print(f"Filtered negative: {len(df_neg_filtered)} rows")