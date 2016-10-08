#!/usr/bin/env python3
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import matplotlib.pyplot as plt
import numpy as np
import data
import os.path
import math
import skimage.io as io
from random import randint
print("Running!")

saveweights = True
filepath = "hintbot_weights_relu_2.h5"

# Input placeholder
original = Input(shape=(32, 32, 4))

# Model layer stack
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(original)
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)
x = Convolution2D(16, 3, 3, activation='relu', border_mode='same')(x)
downscaled = Convolution2D(4, 3, 3, activation='relu', border_mode='same')(x)

# Compile model
hintbot = Model(input=original, output=downscaled)
hintbot.compile(optimizer='adadelta', loss='mean_squared_error')

# Print layer stack so I can figure out why it isn't working
hintbot.summary()

# Prepare input
x,y = data.loadImages("input_iconsets", -1)
# p = np.random.permutation(len(x))
# x = x[p]
# y = y[p]
split = .9
x_train = x[:int(len(x) * split)]
y_train = y[:int(len(y) * split)]
x_test = x[int(len(x) * split):]
y_test = y[int(len(y) * split):]
print("x_train size",len(x_train),"x_test size",len(x_test))

# Train

if (os.path.isfile(filepath) and saveweights):
    hintbot.load_weights(filepath)
hintbot.fit(x_train, y_train, nb_epoch=1, batch_size=8, shuffle=True, validation_data=(x_test, y_test))

# image_test = np.asarray([io.imread("debug.png")])
# io.imsave("debug_output.png", hintbot.predict(image_test).clip(0,255).astype(np.uint8)[0])

# Predict
test_predictions = hintbot.predict(x_test).clip(0,255).astype(np.uint8)

# Save results of tests to a folder
prediction_folder = "test_predictions"
for i in range(0, len(test_predictions)):
    io.imsave(prediction_folder + "/" + str(i) + ".png", test_predictions[i])

# Display some results (code from https://blog.keras.io/building-autoencoders-in-keras.html until I properly learn matplotlib)
n = 10
plt.figure(figsize=(20, 2))
for j in range(n):
    i = randint(0, len(x_test))
    # Display original
    ax = plt.subplot(2, n, j + 1)
    plt.imshow(y_test[i], interpolation='nearest')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display hinting
    ax = plt.subplot(2, n, j + 1 + n)
    plt.imshow(test_predictions[i], interpolation='nearest')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
if (saveweights):
    print("saving weights")
    hintbot.save_weights(filepath, overwrite=True)
plt.show()
