# Libraries
import pandas as pd
import numpy as np
import joblib
#rest is need for AI
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

fileName = 'extracted_features.csv'
data = pd.read_csv(fileName)
print(data.head())

# Select features for the model
features = ['hour_of_day', 'day_of_week', 'times_seen', 'lat', 'lon']

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data[features])

# Initialize the Isolation Forest model
model = IsolationForest(contamination=0.1, random_state=42)

# Fit the model to the data
model.fit(scaled_features)

# Save Model
joblib.dump(model, 'isolation_forest_model.pkl')

print("Model has been trained and saved")