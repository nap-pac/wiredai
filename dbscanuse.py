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
filename = 'test_features2.csv'  # Adjust path as needed
data = pd.read_csv(filename)

# Preprocess the new data (assuming it has the same structure as before)
# Rename columns
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude', 'True_Value']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]

# Save the original latitude and longitude for plotting
original_lat_long = data[['Latitude', 'Longitude']].copy()

# Scale the new features using the loaded scaler
featureScaled = scaler.transform(features)

# Make predictions using the loaded DBSCAN model
clusters = dbscan.fit_predict(featureScaled)

# Add the cluster labels to the new data
data['Cluster'] = clusters

# Analyze the clusters
clusterAnalysis = data.groupby('Cluster').agg(
    DeviceCount=('MAC_Address', 'nunique'),
    TotalTimesSeen=('Times_Seen', 'sum')
).reset_index()

# Print the cluster analysis results
print(clusterAnalysis)

# Separate data into clustered points and noise (cluster = -1)
clustered_data = data[data['Cluster'] != -1]
noise_data = data[data['Cluster'] == -1]

# Use the original latitude and longitude for plotting
clustered_lat_long = original_lat_long.iloc[clustered_data.index]
noise_lat_long = original_lat_long.iloc[noise_data.index]

# Visualize the clusters with true latitude and longitude
plt.figure(figsize=(10, 6))

# Plot clustered points using true latitude and longitude
plt.scatter(clustered_lat_long['Longitude'], clustered_lat_long['Latitude'], 
            c=clustered_data['Cluster'], cmap='viridis', s=10, label='Clustered')

# Plot noise points (outliers detected by DBSCAN)
plt.scatter(noise_lat_long['Longitude'], noise_lat_long['Latitude'], 
            c='r', label='Noise', s=10)

plt.title('DBSCAN Clustering with True Latitude and Longitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.colorbar(label='Cluster Label')
plt.show()