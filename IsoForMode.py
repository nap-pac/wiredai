#Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
#rest is need for AI
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

fileName = 'test_features.csv'
data = pd.read_csv(fileName)
print(data.head())

# Select features for the model
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']
features = ['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']

# Scale the features
scaler = StandardScaler()
scaledFeatures = scaler.fit_transform(data[features])

# Import Model
model = joblib.load('isolation_forest_model.pkl')

# Predict anomalies
data['anomaly'] = model.predict(scaledFeatures)

# Convert anomaly labels (-1 for anomaly, 1 for normal) to a more intuitive format (0 for normal, 1 for anomaly)
data['anomaly'] = data['anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Create a scatter plot to visualize the anomalies
plt.figure(figsize=(10, 6))

# Scatter plot of Main Cluster
normal = data[data['anomaly'] == 0]
plt.scatter(normal['Latitude'], normal['Longitude'], c='blue', label='Main Cluster', alpha=0.5)

# Scatter plot of Anomolous
anomalies = data[data['anomaly'] == 1]
plt.scatter(anomalies['Latitude'], anomalies['Longitude'], c='red', label='Benign', alpha=0.5)

# Adding labels and title
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title('Anomaly Detection in Wi-Fi Data')
plt.legend()
plt.savefig('plot.png', dpi=300)