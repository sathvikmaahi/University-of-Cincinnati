# -*- coding: utf-8 -*-
"""SathvikSanka_neuralnetwork.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VBZ7fo1okG7SsZW_WoGSz6AGefbG35MQ
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from sklearn.metrics import r2_score
import pandas as pd
import seaborn as sns

"""## For this assignment, you should answer the questions in cells 2,4,5,8,10,11,12 (14),13"""

data = pd.read_csv('app_usage.csv')

data.info()

vpn_df = pd.read_csv('/content/app_usage.csv')

#look at the shape of the dataframe
print(vpn_df.shape)

#look at the column names
print(vpn_df.columns)

#show the first 5 records
print(vpn_df.head(5))

# Assuming your DataFrame is named 'vpn_df' and the column is 'RemoteAccess'
sns.histplot(vpn_df['RemoteAccess'], bins=10, kde=True)  # Adjust bins as needed
plt.title('Distribution of Remote VPN Access')
plt.xlabel('Remote VPN Access')
plt.ylabel('Frequency')
plt.show()

#split the dataset into features and target.
#RemoteAccess is the target, we will build a model that
#takes all other columns as X to predict remote VPN usage
#Y the "RemoteAccess" column. X is all other columns (except RemoteAccess)
X = vpn_df.drop('RemoteAccess', axis=1)
Y = vpn_df['RemoteAccess']

#visualize the data
print(X.head(5))
print(Y.head(5))

#set a random seed to achieve consistent results
tf.random.set_seed(0)

#Create a Sequential Neural Network with 5 layers. The layers should have the following units respectively 64,64,54,40,1
#specify appropiate shape as input
#Choose appropiate activation for each unit
#Should the output layer have an activation function? If yes, which activation funtion and why; if No, why?
#Add a dropout layer after each hidden layer (not output layer), with a rate between 0.15 and 0.20

"""Yes, the output layer should have an activation function because for predicting the continuous target variable

"""

model1 = Sequential()
model1.add(Dense(64, activation='relu', input_shape=(X.shape[1],)))  # Input layer with 64 units and ReLU activation
model1.add(Dropout(0.15))  # Dropout layer with rate 0.15
model1.add(Dense(64, activation='relu'))  # Hidden layer with 64 units and ReLU activation
model1.add(Dropout(0.15))  # Dropout layer with rate 0.15
model1.add(Dense(54, activation='relu'))  # Hidden layer with 54 units and ReLU activation
model1.add(Dropout(0.15))  # Dropout layer with rate 0.15
model1.add(Dense(40, activation='relu'))  # Hidden layer with 40 units and ReLU activation
model1.add(Dropout(0.15))  # Dropout layer with rate 0.15
model1.add(Dense(1, activation='linear'))  # Output layer with 1 unit and linear activation

model1.summary()

# split the dataset into testing and training, where testing set is 20% of the datset and the training set is 80%
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)  # Use the same random_

#compile and train the model with appropriate loss function and  metrics. You may also add an optimizer
#Explain why you chose the loss function and metrics
#use only X_train and Y_train for the training with an epochs value of 200

model1.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])
history = model1.fit(X_train, Y_train, epochs=200, verbose=0)  # verbose=0 for silent training

"""The reason for MSE is the loss function which mainly used on regression problems and also predicts the continuos target variables."""

# calculate the RSquared
from sklearn.metrics import r2_score

Y_pred = model1.predict(X_test)  # Predict on the test set
r2 = r2_score(Y_test, Y_pred)

print(f"R-squared: {r2}")

# create two more models (model2 and model3) with different layers and unit.
#compile and train on the same dataset (with the same configurations) as we did for model1
#compute the Rsquared for the two models. and compare them with model1
#Create a figure for the history of your selected metrics like the figure below.
#Note that the figures does not have to be exactly the same since our models differs
# Analyze and explain the differences you observed among the three models

model2 = Sequential()
model2.add(Dense(128, activation='relu', input_shape=(X.shape[1],)))
model2.add(Dropout(0.15))
model2.add(Dense(64, activation='relu'))
model2.add(Dropout(0.15))
model2.add(Dense(32, activation='relu'))
model2.add(Dropout(0.15))
model2.add(Dense(1, activation='linear'))

model2.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])
history2 = model2.fit(X_train, Y_train, epochs=200, verbose=0)

Y_pred2 = model2.predict(X_test)
r2_model2 = r2_score(Y_test, Y_pred2)
print(f"R-squared for Model 2: {r2_model2}")

# Model 3
model3 = Sequential()
model3.add(Dense(32, activation='relu', input_shape=(X.shape[1],)))
model3.add(Dropout(0.20))
model3.add(Dense(16, activation='relu'))
model3.add(Dropout(0.20))
model3.add(Dense(8, activation='relu'))
model3.add(Dropout(0.20))
model3.add(Dense(1, activation='linear'))

model3.compile(optimizer='adam', loss='mse', metrics=['mae', 'mse'])
history3 = model3.fit(X_train, Y_train, epochs=200, verbose=0)

Y_pred3 = model3.predict(X_test)
r2_model3 = r2_score(Y_test, Y_pred3)
print(f"R-squared for Model 3: {r2_model3}")

#this is the accuracy of the model 1:
print(f"R-squared for Model 1: {r2}")

"""The difference between the three models is accuracy and also metrics that has choosen for every model is different and also based on metrics we also get accuracy.

If the model 2 or model 3 has more accuracy than model 1, it suggests that there is change in architecture such as number of layers or units. This may effects in performance of the model.


"""

#plotting the graph of 3 models and their metrics

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

plt.plot(history.history['mae'], label='MAE')
plt.plot(history.history['mse'], label='MSE')

plt.xlabel('Epoch')
plt.ylabel('Metric Value')
plt.title('Training Metrics')
plt.legend()
plt.grid(True)
plt.show()

# plot for model2
plt.figure(figsize=(10, 6))

plt.plot(history2.history['mae'], label='MAE')
plt.plot(history2.history['mse'], label='MSE')

plt.xlabel('Epoch')
plt.ylabel('Metric Value')
plt.title('Training Metrics for Model 2')
plt.legend()
plt.grid(True)
plt.show()

#plot for model 3
plt.figure(figsize=(10, 6))

plt.plot(history3.history['mae'], label='MAE')
plt.plot(history3.history['mse'], label='MSE')

plt.xlabel('Epoch')
plt.ylabel('Metric Value')
plt.title('Training Metrics for Model 3')
plt.legend()
plt.grid(True)
plt.show()

