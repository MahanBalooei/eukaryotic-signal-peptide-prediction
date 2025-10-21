import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

# Load features
features_df = pd.read_csv('features.csv')

# Load labels
labels_df = pd.read_csv('training_with_folds.tsv', sep='\t')
labels_df['label'] = pd.to_numeric(labels_df['label'], errors='coerce').fillna(0).astype(int)

# Merge on Accession
df = features_df.merge(labels_df[['Accession', 'label']], on='Accession')

# Prepare features (X) and labels (y)
X = df.drop(columns=['Accession', 'label'])
y = df['label']

# Define kernels to test
kernels = ['linear', 'rbf', 'poly', 'sigmoid']

# Store results
results = []

# Scale + SVC pipeline
scaler = StandardScaler()

for kernel in kernels:
    pipe = Pipeline([
        ('scaler', scaler),
        ('svc', SVC(kernel=kernel))
    ])
    
    # Perform 5-fold cross-validation
    scores = cross_val_score(pipe, X, y, cv=5, scoring='accuracy')
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

print("✅ Kernel testing complete. Results saved to 'kernel_test_results.csv'.")
