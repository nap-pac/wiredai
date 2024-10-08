# Libraries
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Load the scaed model and scalar
with open('SOMmodel.pkl', 'rb') as f:
    som = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Load New Data
data = pd.read_csv('test_features.csv')  # Replace with the path to your new data

# Select relevant features
features = data.iloc[:, 1:].values  # Adjust according to your dataset structure

# Normalize the new data using the previously saved scaler
normalizedData = scaler.transform(features)

# Step 3: Use the Loaded SOM Model
# Finding the BMU for each observation in the new data
bmuIndices = [som.winner(x) for x in normalizedData]

# Count how many new observations map to each neuron
bmu_counts = Counter(bmuIndices)

# Step 4: Visualize the Results
# Create a grid for BMU counts
somSize = som.get_weights().shape[0]
bmu_matrix = np.zeros((somSize, somSize))

for (i, j), count in bmu_counts.items():
    bmu_matrix[i, j] = count

plt.imshow(bmu_matrix, cmap='hot', interpolation='nearest')
plt.title('New Data BMU Counts on SOM Grid')
plt.xlabel('Neuron X Index')  # Label for the X-axis
plt.ylabel('Neuron Y Index')  # Label for the Y-axis
plt.colorbar(label='Number of Observations')
plt.show()