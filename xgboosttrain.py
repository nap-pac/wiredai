import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

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

    # Feature Engineering
    data['ts_sec'] = pd.to_datetime(data['ts_sec'], unit='s')
    data['hour'] = data['ts_sec'].dt.hour
    data['day_of_week'] = data['ts_sec'].dt.dayofweek

    # Label encode MAC addresses
    le = LabelEncoder()
    data['devmac_encoded'] = le.fit_transform(data['devmac'])

    # Calculate distance between device location and a reference point (your location)
    my_lat, my_lon = 40.7128, -74.0060 # Will need to be changed to a live value eventually

    data['distance_to_me'] = data.apply(lambda row: haversine(row['lat'], row['lon'], my_lat, my_lon), axis=1)

    # Drop irrelevant columns (like raw MAC address and timestamp)
    data.drop(columns=['devmac', 'ts_sec', 'lat', 'lon'], inplace=True)

    # Define features (X) and labels (y)
    X = data.drop(columns=['label'])
    y = data['label'].apply(lambda x: 1 if x == 'benign' else 0)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # XGBoost expects data in DMatrix format, but it can also handle DataFrames directly
    # Scaling the data is optional for XGBoost, as it handles unscaled data well, but it could help with convergence speed
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert the data into XGBoost's DMatrix format (optional but recommended for efficiency)
    dtrain = xgb.DMatrix(X_train_scaled, label=y_train)
    dtest = xgb.DMatrix(X_test_scaled, label=y_test)

    # Train the XGBoost model
    xgb_model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss')
    xgb_model.fit(X_train_scaled, y_train)

    # Make predictions on the test set
    y_pred = xgb_model.predict(X_test_scaled)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f'Accuracy: {accuracy:.4f}')
    print('Confusion Matrix:')
    print(conf_matrix)

if __name__=="__main__":
    main()