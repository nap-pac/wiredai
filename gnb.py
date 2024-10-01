# Libraries
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load dataset
fileName = 'data.csv'
data = pd.read_csv(fileName)
print(data.head())

# Drop MAC add
data.drop('devmac', axis=1, inplace=True)

data = data.fillna(0)

# Extract Features and Labels
y = data['label']
x = data.drop('label', axis=1)

# Split to train test
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.3, random_state=42)

# Initalize
gnb = GaussianNB()

# Train
gnb.fit(xTrain, yTrain)

# Predict
yPred = gnb.predict(xTest)

# Calculate Accuracy
acc = accuracy_score(yTest, yPred)
print(f'Accuracy: {acc}')