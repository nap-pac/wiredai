# Libraries
import pandas as pd
import numpy as np
import joblib
#rest is need for AI
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

fileName = 'combined.csv'
data = pd.read_csv(fileName)

# Select features for the model
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]

# Scale the features
scaler = StandardScaler()
scaledFeatures = scaler.fit_transform(features)

# Initialize the Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.0112, max_samples=256)

# Fit the model to the data
model.fit(scaledFeatures)

# Save Model
joblib.dump(model, 'isolation_forest_model.pkl')

# Save the scaler used for scaling features
scaler_filename = 'scaleriso.joblib'
joblib.dump(scaler, scaler_filename)

print("Model has been trained and saved")