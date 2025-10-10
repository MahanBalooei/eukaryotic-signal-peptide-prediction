import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# --- Load position-specific frequencies ---
with open("frequencies.json", "r") as f:
    freq = json.load(f)

# --- SwissProt background frequencies (from your code) ---
SWISSPROT_FREQ = {
    'A': 0.0825, 'C': 0.0138, 'D': 0.0546, 'E': 0.0671, 'F': 0.0386,
    'G': 0.0707, 'H': 0.0227, 'I': 0.0590, 'K': 0.0579, 'L': 0.0964,
    'M': 0.0241, 'N': 0.0406, 'P': 0.0474, 'Q': 0.0393, 'R': 0.0552,
    'S': 0.0665, 'T': 0.0536, 'V': 0.0685, 'W': 0.0110, 'Y': 0.0292
}

# --- Compute log-odds weights ---
weights = {}
for pos, aa_freqs in freq.items():
    weights[pos] = {aa: np.log2(aa_freqs[aa] / SWISSPROT_FREQ[aa]) for aa in aa_freqs}

# --- Create DataFrame for heatmap ---
df = pd.DataFrame(weights).T
df.index = df.index.astype(int)
df = df.sort_index()

# --- Plot heatmap ---
plt.figure(figsize=(12, 6))
sns.heatmap(df, cmap="coolwarm", center=0, cbar_kws={'label': 'Log₂(Odds Ratio)'}, linewidths=0.5)
plt.title("Amino Acid Log-Odds Weight by Position")
plt.xlabel("Amino Acid")
plt.ylabel("Position")
plt.tight_layout()
plt.show()