# Libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

# Load Data
fileName = 'data.csv'
data = pd.read_csv(fileName)

data = data.dropna()

# Features and Labels
X = data[['ts_sec', 'lat', 'lon', 'signal', 'period']]
y = data['label']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create a kNN classifier instance
# Using k=5 as an example, but consider tuning this parameter
knn = KNeighborsClassifier(n_neighbors=5)

# Train the model on the full dataset
knn.fit(X_scaled, y)

# Perform 10-fold cross-validation
cv_scores = cross_val_score(knn, X_scaled, y, cv=10)

# Print results
print("CV Scores:", cv_scores)
print("CV Average Score:", np.mean(cv_scores))