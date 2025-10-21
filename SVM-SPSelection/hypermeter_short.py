import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load data
features_df = pd.read_csv('features.csv')
labels_df = pd.read_csv('training_with_folds.tsv', sep='\t')
labels_df['label'] = pd.to_numeric(labels_df['label'], errors='coerce').fillna(0).astype(int)

# Merge and prepare X and y
df = features_df.merge(labels_df[['Accession', 'label']], on='Accession')
X = df.drop(columns=['Accession', 'label'])
y = df['label']

# Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC())
])

# Hyperparameter grid
param_grid = {
    'svc__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
    'svc__C': [0.1, 1, 10],
    'svc__gamma': ['scale', 'auto'],         # used in rbf, poly, sigmoid
    'svc__degree': [2, 3, 4],                # used in poly
    'svc__coef0': [0.0, 0.1, 0.5],           # used in poly, sigmoid
}

# GridSearch with 5-fold cross-validation
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid.fit(X, y)

# Best parameters and score
print("✅ Best Accuracy:", grid.best_score_)
print("🏆 Best Parameters:", grid.best_params_)

import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load data
features_df = pd.read_csv('features.csv')
labels_df = pd.read_csv('training_with_folds.tsv', sep='\t')
labels_df['label'] = pd.to_numeric(labels_df['label'], errors='coerce').fillna(0).astype(int)

# Merge and prepare X and y
df = features_df.merge(labels_df[['Accession', 'label']], on='Accession')
X = df.drop(columns=['Accession', 'label'])
y = df['label']

# Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('svc', SVC())
])

# Hyperparameter grid
param_grid = {
    'svc__kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
    'svc__C': [0.1, 1, 10],
    'svc__gamma': ['scale', 'auto'],         # used in rbf, poly, sigmoid
    'svc__degree': [2, 3, 4],                # used in poly
    'svc__coef0': [0.0, 0.1, 0.5],           # used in poly, sigmoid
}

# GridSearch with 5-fold cross-validation
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid.fit(X, y)

# Best parameters and score
print("✅ Best Accuracy:", grid.best_score_)
print("🏆 Best Parameters:", grid.best_params_)

# Save best result to CSV
best_result = pd.DataFrame([{
    'best_accuracy': grid.best_score_,
    **grid.best_params_
}])
best_result.to_csv('best_svm_params.csv', index=False)
print("📁 Best result saved to 'best_svm_params.csv'")
