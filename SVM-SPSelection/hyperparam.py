import pandas as pd
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVR, SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv('features.csv')
features = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', 
            'pos_fraction_N5', 'molecular_weight', 'helix_prop', 'sheet_prop', 'coil_prop', 'avg_hydro', 'max_hydro']
X = df[features]
y = df['net_charge']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline for scaling
pipe = Pipeline([('scaler', StandardScaler()), ('svr', SVR())])

# Grid search for linear kernel
param_grid_linear = {'svr__C': [0.1, 1, 10, 100, 1000]}
grid_linear = GridSearchCV(pipe, param_grid_linear, cv=5, scoring='r2')
grid_linear.fit(X_train, y_train)
print('Best linear:', grid_linear.best_params_, 'R2:', grid_linear.best_score_)

# Grid search for RBF kernel
param_grid_rbf = {'svr__C': [0.1, 1, 10, 100], 'svr__gamma': ['scale', 'auto', 0.001, 0.01, 0.1]}
grid_rbf = GridSearchCV(pipe, param_grid_rbf, cv=5, scoring='r2')
grid_rbf.fit(X_train, y_train)
print('Best RBF:', grid_rbf.best_params_, 'R2:', grid_rbf.best_score_)

# Grid search for poly kernel
param_grid_poly = {'svr__C': [0.1, 1, 10], 'svr__gamma': ['scale', 0.001, 0.01], 
                   'svr__degree': [2, 3], 'svr__coef0': [0, 1]}
grid_poly = GridSearchCV(pipe, param_grid_poly, cv=5, scoring='r2')
grid_poly.fit(X_train, y_train)
print('Best poly:', grid_poly.best_params_, 'R2:', grid_poly.best_score_)

# Save results to CSV
results = []
for name, grid in [('linear', grid_linear), ('rbf', grid_rbf), ('poly', grid_poly)]:
    results.append({'kernel': name, 'best_params': str(grid.best_params_), 'best_r2': grid.best_score_})
df_results = pd.DataFrame(results)
df_results.to_csv('hyperparam_results.csv', index=False)
print("Results saved to hyperparam_results.csv")
