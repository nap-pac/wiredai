# Libraries
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

# Calculate distance (in kilometers) between two lat/lon pairs
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def main():
    # Import data
    fileName = 'data.csv'
    data = pd.read_csv(fileName)

    # Convert timestamp to useful time features (e.g., hour of day, day of week)
    data['ts_sec'] = pd.to_datetime(data['ts_sec'], unit='s')
    data['hour'] = data['ts_sec'].dt.hour
    data['day_of_week'] = data['ts_sec'].dt.dayofweek

    # Label encode the MAC addresses if you want to include them as features
    le = LabelEncoder()
    data['devmac_encoded'] = le.fit_transform(data['devmac'])

    # You may want to compute distance from a reference point (your location) using haversine formula
    # Example reference point (your position)
    my_lat, my_lon = 40.7128, -74.0060

    data['distance_to_me'] = data.apply(lambda row: haversine(row['lat'], row['lon'], my_lat, my_lon), axis=1)

    # Drop irrelevant or non-numerical columns (like raw MAC address and raw timestamp)
    data.drop(columns=['devmac', 'ts_sec', 'lat', 'lon'], inplace=True)

    # Define the features and the target variable
    X = data.drop(columns=['label'])  # All features except the label
    y = data['label'].apply(lambda x: 1 if x == 'benign' else 0)  # Binary encoding of the label

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features for SVM
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train an SVM classifier
    svm_model = SVC(kernel='linear')  # You can also experiment with 'rbf' kernel
    svm_model.fit(X_train_scaled, y_train)

    # After training your SVM model (from previous code)
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train_scaled, y_train)

    # Save the model to disk
    joblib.dump(svm_model, 'svm_model.joblib')

    # Optionally, you can also save the scaler to ensure the test data is scaled the same way
    joblib.dump(scaler, 'scaler.joblib')

    print("Model and scaler saved successfully.")

if __name__=="__main__":
    main()