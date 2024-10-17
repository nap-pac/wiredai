# Libraries
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Load the dataset
filePath = 'extracted_features.csv'  # Adjust path as needed
data = pd.read_csv(filePath)

# Features
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]

# Scale the features
scaler = StandardScaler()
featuresScaled = scaler.fit_transform(features)

# Fit the DBSCAN model
dbscan = DBSCAN(algorithm='kd_tree', eps=0.1, min_samples=5)
clusters = dbscan.fit_predict(featuresScaled)

# Add cluster labels to the original dataset
data['Cluster'] = clusters

# Save the DBSCAN model
model_filename = 'dbscan_model.joblib'
joblib.dump(dbscan, model_filename)

# Save the scaler used for scaling features
scaler_filename = 'scaler.joblib'
joblib.dump(scaler, scaler_filename)