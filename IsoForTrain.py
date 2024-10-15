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
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']]

# Scale the features
scaler = StandardScaler()
scaledFeatures = scaler.fit_transform(features)

# Initialize the Isolation Forest model
model = IsolationForest(contamination=0.1, random_state=42)

# Fit the model to the data
model.fit(scaledFeatures)

# Save Model
joblib.dump(model, 'isolation_forest_model.pkl')

print("Model has been trained and saved")