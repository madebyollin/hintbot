#!/usr/bin/env python3
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, AveragePooling2D
from keras.models import Model
import matplotlib
matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
import numpy as np
import data
import os
import math
import warnings
import skimage.io as io
from random import randint
import argparse
import colorutils

# Argument parser
parser = argparse.ArgumentParser(description='Downscale icons while preserving crispness',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
add_arg = parser.add_argument
add_arg("files", nargs="*", default=[])
add_arg("--weights", default=None, type=str, help='h5 file to read/write weights to.')
add_arg("--loadweights", default="weights.h5", type=str, help='h5 file to read weights from.')
add_arg("--saveweights", default="weights.h5", type=str, help='h5 file to write weights to.')
add_arg("--epochs", default=10, type=int, help='h5 file to write weights to.')
add_arg("--predictionfolder", default="predictions", type=str, help="Folder to save predictions in")
add_arg("--updateweb", action='store_true', help='Update the model/weights stored in /web/')

# Determine paths for weights
args = parser.parse_args()
load_weights_filepath = args.loadweights
save_weights_filepath = args.saveweights
weights_filepath = args.weights
if (weights_filepath):
    load_weights_filepath = weights_filepath
    save_weights_filepath = weights_filepath

def createModel():
    # Input placeholder
    original = Input(shape=(None, None, 4))

    # Model layer stack
    x = original
    # x = ZeroPadding2D(padding=(2, 2))(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = Convolution2D(16, 3, 3, activation='linear', border_mode='same')(x)
    x = AveragePooling2D((2, 2), border_mode='valid')(x)
    x = Convolution2D(4, 3, 3, activation='linear', border_mode='same')(x)
    # x = Cropping2D(cropping=((1, 1), (1,1)))(x)
    downscaled = x

    # Compile model
    hintbot = Model(input=original, output=downscaled)
    hintbot.compile(optimizer='adadelta', loss='mean_squared_error')
    # Train
    if (os.path.isfile(load_weights_filepath)):
        hintbot.load_weights(load_weights_filepath)
    return hintbot

hintbot = createModel()

if (args.updateweb):
    print("Saving weights and model to /web...")
    save_weights_web_filepath = "web/hintbot.h5"
    save_model_web_filepath = "web/hintbot.json"
    hintbot.save_weights(save_weights_web_filepath, overwrite=True)
    import encoder
    enc = encoder.Encoder(save_weights_web_filepath)
    enc.serialize()
    enc.save()
    with open(save_model_web_filepath, 'w') as f:
        f.write(hintbot.to_json())

if len(args.files) > 0:
    x_test = np.asarray([io.imread(filepath) for filepath in args.files])
else:
    # Prepare input
    x_train, y_train, x_test, y_test = data.loadImages("input_iconsets", -1)


    hintbot.fit(x_train, y_train, nb_epoch=args.epochs, batch_size=8, shuffle=True, validation_data=(x_test, y_test))

    # Save weights
    if (save_weights_filepath):
        print("saving weights")
        hintbot.save_weights(save_weights_filepath, overwrite=True)

# Predict test set
test_predictions = hintbot.predict(x_test).clip(0,255).astype(np.uint8)

# Save results on test set to a folder
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    io.imsave
if not os.path.exists(args.predictionfolder):
    os.makedirs(args.predictionfolder)
for i in range(0, len(test_predictions)):
    filename = str(i) + ".png"
    io.imsave(args.predictionfolder + "/" + filename, test_predictions[i])
