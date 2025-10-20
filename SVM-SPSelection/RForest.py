import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

# Load data
df = pd.read_csv('features.tsv', sep='\t')

# Assume 'net_charge' as target (regression); adjust if needed
target_col = 'net_charge'
X = df.drop(columns=[target_col])
y = df[target_col]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit RandomForest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Feature importances
importances = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

# Select top 10 features (adjust threshold or n as needed)
top_features = importances.head(10)['feature'].tolist()

# Save results
importances.to_csv('feature_importances.csv', index=False)
with open('selected_features.txt', 'w') as f:
    f.write('Top 10 selected features:\n' + '\n'.join(top_features))

print("Feature selection complete. Check 'feature_importances.csv' and 'selected_features.txt'.")