from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
import matplotlib.pyplot as plt
import data
import os.path
import math
import random
import skimage.io as io
import numpy as np

# Trying to figure out why my model can't learn the identity function
# Simple hacked together bits and pieces

inputImages = np.asarray([io.imread("debug.png")])

print("shape is:",inputImages.shape)
# ('shape is:', (1, 32, 32, 4))

# Input placeholder
original = Input(shape=(32, 32, 4))

# Model layer stack
downscaled = Convolution2D(4, 3, 3, activation='linear', border_mode='same', init='uniform')(original)

# Compile model
hintbot = Model(input=original, output=downscaled)
hintbot.compile(optimizer='adadelta', loss='mean_squared_error')

# Print layer stack so I can figure out why it isn't working
hintbot.summary()

# Prepare input
x = inputImages

# Train
hintbot.fit(x, x, nb_epoch=100, batch_size=1, shuffle=True, validation_data=(x, x))

# Predict
test_predictions = hintbot.predict(x)

# Display some results (code from https://blog.keras.io/building-autoencoders-in-keras.html until I properly learn matplotlib)

plt.figure(figsize=(8, 4))
# Display original
ax = plt.subplot(221)
plt.imshow(x[0])
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

# Display hinting
ax = plt.subplot(222)
plt.imshow(test_predictions[0])
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.show()
