import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load features with Accession
features_df = pd.read_csv('features.csv')

# Load labels (from TSV file)
labels_df = pd.read_csv('training_with_folds.tsv', sep='\t')
labels_df['label'] = pd.to_numeric(labels_df['label'], errors='coerce').fillna(0).astype(int)

# Merge on Accession
merged_df = features_df.merge(labels_df[['Accession', 'label']], on='Accession')

# Prepare X and y
X = merged_df.drop(columns=['Accession', 'label'])
y = merged_df['label']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Fit Random Forest for feature selection
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Extract feature importances
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values(by='importance', ascending=False)

# Save to CSV
importances.to_csv('feature_importances.csv', index=False)
print("✅ Feature importances saved to 'feature_importances.csv'")






