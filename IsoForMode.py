#Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
#rest is need for AI
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

fileName = 'test_features2.csv'
data = pd.read_csv(fileName)

# Select features for the model
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude', 'True_Label']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]

# Save original latitude and longitude for plotting later
original_lat_long = data[['Latitude', 'Longitude']].copy()

# Scale the features
scaler = joblib.load('scaler.pkl')  # make sure you save this during model training
scaledFeatures = scaler.transform(features)

# Import Model
model = joblib.load('isolation_forest_model.pkl')

# Predict anomalies
data['anomaly'] = model.predict(scaledFeatures)

# Convert anomaly labels (-1 for anomaly, 1 for normal) to a more intuitive format (0 for normal, 1 for anomaly)
data['anomaly'] = data['anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Scatter plot of Main Cluster (Normal points)
normal = data[data['anomaly'] == 0]
plt.scatter(original_lat_long.loc[normal.index, 'Longitude'], 
            original_lat_long.loc[normal.index, 'Latitude'], 
            c='blue', label='Normal', alpha=0.5)

# Scatter plot of Anomalous points (Outliers)
anomalies = data[data['anomaly'] == 1]
plt.scatter(original_lat_long.loc[anomalies.index, 'Longitude'], 
            original_lat_long.loc[anomalies.index, 'Latitude'], 
            c='red', label='Anomoly', alpha=0.5)

# Adding labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Anomaly Detection in Wi-Fi Data')
plt.legend()
plt.savefig('plot.png', dpi=300)