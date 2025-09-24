import pandas as pd

# Load the TSV file
df_train = pd.read_csv('training_set.tsv', sep='\t')

# Print and save inspection results
columns_info = f"Columns in training_set.tsv: {df_train.columns.tolist()}"
head_info = f"\nFirst few rows:\n{df_train.head().to_string()}"

# Print to console
print(columns_info)
print(head_info)

# Save to a text file for reference
with open('training_set_inspection.txt', 'w') as f:
    f.write(columns_info + '\n\n' + head_info)

print("\nInspection results saved to 'training_set_inspection.txt'")