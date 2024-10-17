# Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, precision_recall_curve

# Load the data
fileName = 'test_features4.csv'
data = pd.read_csv(fileName)

# Define columns
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude', 'True_Label']
# Select features for the model
features = data[['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Longitude', 'Latitude']]
true_labels = data[['True_Label']]  # True anomaly labels

# Save original latitude and longitude for plotting later
original_lat_long = data[['Latitude', 'Longitude']].copy()

# Load scaler and model
scaler = joblib.load('scaleriso.joblib') 
model = joblib.load('isolation_forest_model.pkl')

# Scale the features using the loaded scaler
scaledFeatures = scaler.transform(features)

# Predict anomalies
data['anomaly'] = model.predict(scaledFeatures)
data['anomaly'] = data['anomaly'].apply(lambda x: 1 if x == -1 else 0)

# Calculate metrics
accuracy = accuracy_score(true_labels, data['anomaly'])
precision = precision_score(true_labels, data['anomaly'])
recall = recall_score(true_labels, data['anomaly'])
f1 = f1_score(true_labels, data['anomaly'])
conf_matrix = confusion_matrix(true_labels, data['anomaly'])

# Print the results
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)

# Plotting
plt.figure(figsize=(10, 6))
normal = data[data['anomaly'] == 0]
anomalies = data[data['anomaly'] == 1]
plt.scatter(original_lat_long.loc[normal.index, 'Longitude'], original_lat_long.loc[normal.index, 'Latitude'], c='blue', label='Normal', alpha=0.7, marker='o')
plt.scatter(original_lat_long.loc[anomalies.index, 'Longitude'], original_lat_long.loc[anomalies.index, 'Latitude'], c='red', label='Anomaly', alpha=0.7, marker='x')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Anomaly Detection in Wi-Fi Data')
plt.legend()
plt.grid(True)
plt.savefig('plot.png', dpi=300)
plt.show()