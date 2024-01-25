import tensorflow as tf
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2

def plot_predictions(model, x, y, start=0, end=100):
    predictions = model.predict(x).flatten()
    df = pd.DataFrame(data={'Predictions':predictions, 'Actuals':y})
    return df, mse(y, predictions)

def df_to_X_y(df, window_size=5):
  df_as_np = df.to_numpy()
  X = []
  y = []
  for i in range(len(df_as_np)-window_size):
    row = [[a] for a in df_as_np[i:i+window_size]]
    X.append(row)
    label = df_as_np[i+window_size]
    y.append(label)
  return np.array(X), np.array(y)

def dateConversion(date):
    suffix = ""
    splitDates = date.split("-")
    if splitDates[2].startswith('0'):
        splitDates[2] = splitDates[2][1:]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    if 10 <= int(splitDates[2]) % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(int(splitDates[2]) % 10, "th")
    return f"{str(splitDates[2]) + suffix} of {months[int(splitDates[1]) - 1]}"

# Apply a moving average to the predictions for smoother plots
def moving_average(data, window_size):
    cumsum = np.cumsum(data)
    cumsum[window_size:] = cumsum[window_size:] - cumsum[:-window_size]
    return np.concatenate([np.full(window_size - 1, np.nan), cumsum[window_size - 1:] / window_size]) * 3.65

def find_best_snow_period(model, x, window_days, data):
    # Calculate the number of samples corresponding to the window size
    window_samples = window_days 

    best_period_start = None
    best_period_end = None
    best_snow_prediction = 0.0  # Set a threshold for snow presence

    for i in range(len(x) - window_samples + 1):
        # Get predictions within the rolling window
        window_predictions = model.predict(x[i:i+window_samples]).flatten()
        average_prediction = np.mean(window_predictions)

        # Check if the average prediction suggests snow and update best period
        if average_prediction > best_snow_prediction:
            best_snow_prediction = average_prediction
            best_period_start = data[i]
            best_period_end = data[i + window_samples - 1]

    if best_snow_prediction > 0.5:
        return best_period_start, best_period_end, best_snow_prediction
    else:
        return 0,0,0
    
def recommend(data_io, duration_param):    
    # Data Preprocessing
    data = pd.read_csv(data_io)
    data.index = pd.to_datetime(data['datetime'], format='%Y-%m-%d')

    temp = data['snowdepth']

    WINDOW_SIZE = 7
    X1, y1 = df_to_X_y(temp, WINDOW_SIZE)

    # Data Splitting
    # Splitting data into training, validation, and test sets
    train_size = int(len(X1) * 0.7)
    val_size = int(len(X1) * 0.15)

    X_train1, y_train1 = X1[:train_size], y1[:train_size]
    X_val1, y_val1 = X1[train_size : train_size + val_size], y1[train_size : train_size + val_size]
    X_test1, y_test1 = X1[train_size + val_size:], y1[train_size + val_size:]

    # Model Building
    model1 = Sequential()
    model1.add(InputLayer((WINDOW_SIZE, 1)))
    model1.add(LSTM(64, return_sequences=False, kernel_regularizer=l2(0.01)))
    model1.add(Dropout(0.2))
    model1.add(Dense(32, activation='relu'))
    model1.add(Dense(1, activation='linear'))

    model1.summary()

    # Compile and Train the Model
    model1.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001), metrics=['RootMeanSquaredError'])
    history = model1.fit(X_train1, y_train1, validation_data=(X_val1, y_val1), epochs=500, batch_size=7)

    # Combine training, validation, and test sets
    X_combined = np.concatenate((X_train1, X_val1, X_test1), axis=0)

    # Make predictions on the entire dataset
    combined_predictions = model1.predict(X_combined)
    # Plotting Predictions on the entire dataset
    ##plt.plot(combined_predictions, label='Predicted Snow')
    ##plt.legend()
    ##plt.title('Yearly Forecast')
    ##plt.show()

    window_days = int(duration_param)
    best_start, best_end, best_snow = find_best_snow_period(model1, X_combined, window_days, pd.read_csv('weather_data.csv')['datetime'])
    if best_start and best_end and best_snow == 0:
        print(f"No significant snow predicted in any {duration_param}-day window.")
    else:
        print("Best snow period start:", best_start)
        print("Best snow period end:", best_end)
        print(f"There will be an average of {round(best_snow)} inches of snow")
        print("Best snow period start:", dateConversion(best_start))
        print("Best snow period end:", dateConversion(best_end))
        return best_start, best_end, dateConversion(best_start), dateConversion(best_end), round(best_snow), combined_predictions