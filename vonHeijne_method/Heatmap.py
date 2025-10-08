import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the matrix
df = pd.read_csv("frequency_matrix.csv", index_col=0)

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df, cmap="viridis", annot=False)

plt.title("Frequency Heatmap", fontsize=14)
plt.xlabel("Columns")
plt.ylabel("Rows")

# Save as PNG
plt.savefig("heatmap.png", dpi=300, bbox_inches='tight')
plt.show()