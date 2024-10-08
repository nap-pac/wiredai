# Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix

# Import data
fileName = 'data.csv'
data = pd.read_csv(fileName)

# Label encode categorical features
le = LabelEncoder()
data['devmac_encoded'] = le.fit_transform(data['devmac'])

# Prepare the feature set (X) and target labels (y)
# Use latitude, longitude, signal, period, and the encoded device MAC address as features
X = data[['lat', 'lon', 'signal', 'period', 'devmac_encoded']]

# 1 = benign, 0 = following
y = data['label'].apply(lambda x: 1 if x == 'benign' else 0)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the SVM model using the scaled features
svm_model = SVC(kernel='linear')  # You can experiment with other kernels like 'rbf'
svm_model.fit(X_train_scaled, y_train)

# Make predictions and evaluate the model
y_pred = svm_model.predict(X_test_scaled)

# Evaluate the model performance
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f'Accuracy: {accuracy:.4f}')
print('Confusion Matrix:')
print(conf_matrix)