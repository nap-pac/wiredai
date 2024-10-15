# Libraries
import pandas as pd
import joblib
from sklearn import svm
from sklearn.preprocessing import StandardScaler

# Load Data
fileName = 'extracted_features.csv'
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

# Save the trained model
joblib.dump(one_class_svm, 'one_class_svm_model.pkl')

# Save the scaler as well, to use the same scaling for new data
joblib.dump(scaler, 'onescaler.pkl')

print("Model and scaler saved successfully!")