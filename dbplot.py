import matplotlib.pyplot as plt
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D  # For custom legends

# Load the DBSCAN model and scaler
dbscan = joblib.load('dbscan_model.joblib')
scaler = joblib.load('scaler.joblib')

# Load new data for prediction
data = pd.read_csv('test_features2.csv')
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude', 'True_Value']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]

# Scale the new features using the loaded scaler
featureScaled = scaler.transform(features)

# Make predictions using the loaded DBSCAN model
clusters = dbscan.fit_predict(featureScaled)
data['Cluster'] = clusters

# Separate data into clustered points and noise
clustered_data = data[data['Cluster'] != -1]
noise_data = data[data['Cluster'] == -1]

# Map each cluster to a different marker
marker_list = ['o', 'v', '^', '<', '>', 's', 'p', '*', '+', 'x', 'd']
unique_clusters = clustered_data['Cluster'].unique()
cluster_marker = {cluster: marker_list[i % len(marker_list)] for i, cluster in enumerate(unique_clusters)}

# Plotting
plt.figure(figsize=(10, 8))
plt.subplots_adjust(right=0.75)

# Plot clustered points using true latitude and longitude
for cluster, marker in cluster_marker.items():
    cluster_points = clustered_data[clustered_data['Cluster'] == cluster]
    plt.scatter(cluster_points['Longitude'], cluster_points['Latitude'], marker=marker, label=f'Cluster {cluster}', alpha=0.7)

# Plot noise points (outliers detected by DBSCAN)
plt.scatter(noise_data['Longitude'], noise_data['Latitude'], color='red', label='Noise', marker='x', alpha=0.7)

plt.title('DBSCAN Clustering with True Latitude and Longitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')

# Customize legend to handle multiple markers
legend_elements = [Line2D([0], [0], marker=marker, color='w', markerfacecolor='gray', markersize=10, label=f'Cluster {cluster}')
                   for cluster, marker in cluster_marker.items()]
legend_elements.append(Line2D([0], [0], marker='x', color='w', markerfacecolor='red', markersize=10, label='Noise'))
plt.legend(handles=legend_elements, title='Clusters', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.show()