import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

# Load data
df = pd.read_csv('features.csv')

# Assume 'net_charge' as target; use all features for simplicity
# For classification with SVC, binarize the continuous target (e.g., positive vs non-positive)
target_col = 'net_charge'
X = df.drop(columns=[target_col])
y = df[target_col]
y = (y > 0).astype(int)  # Binarize: 1 for positive net_charge, 0 otherwise

# Define kernels to test
kernels = ['linear', 'rbf', 'poly', 'sigmoid']

# Results storage
results = []

# Scale features
scaler = StandardScaler()

for kernel in kernels:
    # Pipeline: scale + SVC
    pipe = Pipeline([('scaler', scaler), ('svc', SVC(kernel=kernel))])
    
    # Cross-validation (5-fold) for accuracy score
    # Adjust scoring as needed (e.g., 'f1' for imbalanced classes)
    scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')
    
    # Mean and std
    mean_score = np.mean(scores)
    std_score = np.std(scores)
    
    results.append({
        'kernel': kernel,
        'mean_accuracy': mean_score,
        'std_accuracy': std_score
    })
    
    print(f"Kernel: {kernel}, Mean Accuracy: {mean_score:.4f} (+/- {std_score:.4f})")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv('kernel_test_results.csv', index=False)

print("Kernel testing complete. Results saved to 'kernel_test_results.csv'.")