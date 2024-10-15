# Libraries
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load the saved model and scaler
one_class_svm = joblib.load('one_class_svm_model.pkl')
scaler = joblib.load('onescaler.pkl')

# Load the data for prediction (same structure as training data)
fileName = 'extracted_features.csv'
data = pd.read_csv(fileName)

# Select features
data.columns = ['MAC_Address', 'Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']
features = ['Hour_of_Day', 'Day_of_Week', 'Times_Seen', 'Latitude', 'Longitude']

# Scale the new data using the loaded scaler
features_scaled = scaler.transform(data[features])

# Predict anomalies using the loaded model
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