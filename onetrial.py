# Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.preprocessing import StandardScaler

# Load Data
fileName = 'test_features.csv'
data = pd.read_csv(fileName)
print(data.head())

# Select features for the model
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']]

# Scale the data
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Train One-Class SVM (assuming you are using only normal data for training)
one_class_svm = svm.OneClassSVM(kernel='rbf', gamma=0.001, nu=0.05)
one_class_svm.fit(features_scaled)

# Predict anomalies (outliers will be labeled as -1, normal data as 1)
predictions = one_class_svm.predict(features_scaled)

# Add the predictions to your data
data['Anomaly'] = predictions

# Separate normal and anomalous points
normal_data = data[data['Anomaly'] == 1]
anomalous_data = data[data['Anomaly'] == -1]

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(normal_data['Longitude'], normal_data['Latitude'], c='b', label='Normal', s=10)
plt.scatter(anomalous_data['Longitude'], anomalous_data['Latitude'], c='r', label='Anomaly', s=10)
plt.title('One-Class SVM Anomaly Detection')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()