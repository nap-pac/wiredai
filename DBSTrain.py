# Libraries
import pandas as pd
import numpy as np
import pickle
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

# Analyze the clusters
clusterAnalysis = data.groupby('Cluster').agg(
    DeviceCount=('MAC_Address', 'nunique'),
    AverageLatitude=('Latitude', 'mean'),
    AverageLongitude=('Longitude', 'mean'),
    TotalTimesSeen=('Times_Seen', 'sum')
).reset_index()

# Print the cluster analysis results
print(clusterAnalysis)

# Save the model
with open('DBSModel.pk1', 'wb') as f:
    pickle.dump(dbscan, f)