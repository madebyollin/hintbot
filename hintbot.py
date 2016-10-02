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

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(original)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
downscaled = Convolution2D(4, 3, 3, activation='relu', border_mode='same')(x)

hintbot = Model(input=original, output=downscaled)

hintbot.compile(optimizer='adadelta', loss='mean_squared_error')

# Prepare input
x,y = data.loadImages("input_iconsets")

x_train = x[:int(len(x) * .9)]
y_train = y[:int(len(x) * .9)]
x_test = x[int(len(x) * .9):]
y_test = y[int(len(x) * .9):]
print("sizes:")
print(x_train.size)
print(x_test.size)

hintbot.summary()
if (os.path.isfile(filepath)):
    hintbot.load_weights(filepath)
hintbot.fit(x_train, y_train, nb_epoch=5, batch_size=32, shuffle=True, validation_data=(x_test, y_test))

# encode and decode some digits
decoded_imgs = hintbot.predict(x_test)

n = 10  # how many we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
hintbot.save_weights(filepath, overwrite=True)
plt.show()
