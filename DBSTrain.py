# Libraries
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Load the dataset
filePath = 'extracted_features.csv'  # Adjust path as needed
data = pd.read_csv(filePath)

# Rename columns for easier reference
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']

# Select relevant features for clustering
features = data[['Latitude', 'Longitude', 'Times_Seen']]

# Scale the features
scaler = StandardScaler()
featuresScaled = scaler.fit_transform(features)

# Fit the DBSCAN model
dbscan = DBSCAN(eps=0.5, min_samples=5)  # Parameters can be tuned
clusters = dbscan.fit_predict(featuresScaled)

# Add cluster labels to the original dataset
data['Cluster'] = clusters

# Save the DBSCAN model
model_filename = 'dbscan_model.joblib'
joblib.dump(dbscan, model_filename)

# Save the scaler used for scaling features
scaler_filename = 'scaler.joblib'
joblib.dump(scaler, scaler_filename)