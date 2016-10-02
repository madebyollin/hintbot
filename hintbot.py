#!/usr/bin/env python3
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import matplotlib.pyplot as plt
import numpy as np
import data
import os.path
import math
print("Running!")

filepath = "hintbot_weights.h5"

# Input placeholder
original = Input(shape=(32, 32, 4))

# Model layer stack
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(original)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
downscaled = Convolution2D(4, 3, 3, activation='relu', border_mode='same')(x)

# Compile model
hintbot = Model(input=original, output=downscaled)
hintbot.compile(optimizer='adadelta', loss='mean_squared_error')

# Print layer stack so I can figure out why it isn't working
hintbot.summary()

# Prepare input
x,y = data.loadImages("input_iconsets")
split = .9
x_train = x[:int(len(x) * split)]
y_train = y[:int(len(y) * split)]
x_test = x[int(len(x) * split):]
y_test = y[int(len(y) * split):]

# Train

if (os.path.isfile(filepath)):
    hintbot.load_weights(filepath)
hintbot.fit(x_train, y_train, nb_epoch=5, batch_size=32, shuffle=True, validation_data=(x_test, y_test))

# Predict
test_predictions = hintbot.predict(x_test)

# Display some results (code from https://blog.keras.io/building-autoencoders-in-keras.html until I properly learn matplotlib)
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display hinting
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(test_predictions[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
hintbot.save_weights(filepath, overwrite=True)
plt.show()
