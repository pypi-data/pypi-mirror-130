# load libraries
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from timewarpy import preprocess, datasets

# load and preprocess
df = datasets.load_energy_data()
X, y = preprocess.create_univariate_windows(df, 1000, 100, 'Appliances')
max_val = X.max()
X = X/max_val
y = y/max_val
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
print(f'Original dataframe shape: {df.shape}')
print(f'X training vector shape: {X_train.shape}')
print(f'y training vector shape: {y_train.shape}')

# train small tensorflow model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.LSTM(10, activation='tanh', recurrent_activation='sigmoid',
                               return_sequences=False, input_shape=X_train[0].shape))
model.add(tf.keras.layers.Dense(100))
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss='mean_squared_error',
)
history = model.fit(
    X_train,
    y_train,
    epochs=2,
    batch_size=100,
)

# make predictions
y_pred = model.predict(X_test)
mae = np.mean(np.abs(y_test - y_pred)) * max_val
print(f'y prediction vector shape: {y_pred.shape}')
print(f'Model Mean Absolute Error: {mae:.2f}')
