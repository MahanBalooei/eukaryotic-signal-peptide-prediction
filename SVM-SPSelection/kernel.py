import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

# Load data
df = pd.read_csv('features.tsv', sep='\t')

# Assume 'net_charge' as target; use all features for simplicity
target_col = 'net_charge'
X = df.drop(columns=[target_col])
y = df[target_col]

# Define kernels to test
kernels = ['linear', 'rbf', 'poly', 'sigmoid']

# Results storage
results = []

# Scale features
scaler = StandardScaler()

for kernel in kernels:
    # Pipeline: scale + SVR
    pipe = Pipeline([('scaler', scaler), ('svr', SVR(kernel=kernel))])
    
    # Cross-validation (5-fold) for R2 score
    scores = cross_val_score(pipe, X, y, cv=5, scoring='r2')
    
    # Mean and std
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    
    results.append({
        'kernel': kernel,
        'mean_r2': mean_score,
        'std_r2': std_score
    })
    
    print(f"Kernel: {kernel}, Mean R2: {mean_score:.4f} (+/- {std_score:.4f})")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('kernel_test_results.csv', index=False)

print("Kernel testing complete. Results saved to 'kernel_test_results.csv'.")