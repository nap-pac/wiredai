# Libraries
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the DBSCAN model
model_filename = 'dbscan_model.joblib'
dbscan = joblib.load(model_filename)

# Load the scaler
scaler_filename = 'scaler.joblib'
scaler = joblib.load(scaler_filename)

# Load new data for prediction
filename = 'test_features.csv'  # Adjust path as needed
data = pd.read_csv(filename)

# Preprocess the new data (assuming it has the same structure as before)
# Rename columns
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']
features = data[['Latitude', 'Longitude', 'Times_Seen']]

# Scale the new features using the loaded scaler
featureScaled = scaler.transform(features)

# Make predictions using the loaded DBSCAN model
clusters = dbscan.fit_predict(featureScaled)

# Add the cluster labels to the new data
data['Cluster'] = clusters

# Analyze the clusters
cluster_analysis = data.groupby('Cluster').agg(
    Device_Count=('MAC_Address', 'nunique'),
    Average_Latitude=('Latitude', 'mean'),
    Average_Longitude=('Longitude', 'mean'),
    Total_Times_Seen=('Times_Seen', 'sum')
).reset_index()

# Print the cluster analysis results
print(cluster_analysis)


# Visualize the clusters
plt.figure(figsize=(10, 6))
plt.scatter(data['Longitude'], data['Latitude'], c=data['Cluster'], cmap='viridis', s=10)
plt.title('DBSCAN Clustering of Device Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(label='Cluster Label')
plt.show()