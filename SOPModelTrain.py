# Libraries
import pandas as pd
import numpy as np
import matplotlib as plt
import pickle
from sklearn.preprocessing import MinMaxScaler
from minisom import MiniSom

# Import data
fileName = 'extracted_features.csv'
data = pd.read_csv(fileName)

# Select Features
features = data.iloc[:, 1:].values
scaler = MinMaxScaler()
normalizedData = scaler.fit_transform(features)

# Create SOM Model
som_size = 100
som = MiniSom(som_size, som_size, normalizedData.shape[1], sigma=1.0, learning_rate=0.5)

# Train model
som.train(normalizedData, num_iteration=1000)

# Save the model
with open('SOMmodel.pkl', 'wb') as f:
    pickle.dump(som, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)