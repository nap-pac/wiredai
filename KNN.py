# Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load Data
fileName = 'data.csv'
data = pd.read_csv(fileName)

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