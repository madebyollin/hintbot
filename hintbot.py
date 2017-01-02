#!/usr/bin/env python3
from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, AveragePooling2D
from keras.models import Model
from scipy.misc import imresize
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
add_arg("--epochs", default=10, type=int, help='Number of epochs to train.')
add_arg("--split", default=0.95, type=float, help='Percent of the data to train on.')
add_arg("--predictionfolder", default="predictions", type=str, help="Folder to save predictions in")
add_arg("--updateweb", action='store_true', help='Update the model/weights stored in /web/')
add_arg("--makeiconset", action='store_true', help='Create a full iconset from the provided file')


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

def predict(model, x):
    x = np.asarray([x])
    return model.predict(x).clip(0,255).astype(np.uint8)[0]

def train(model):
    # Prepare input
    x_train, y_train, x_test, y_test = data.loadImages("input_iconsets", -1, args.split)
    hintbot.fit(x_train, y_train, nb_epoch=args.epochs, batch_size=8, shuffle=True, validation_data=(x_test, y_test))

    # Save weights
    if (save_weights_filepath):
        print("saving weights")
        hintbot.save_weights(save_weights_filepath, overwrite=True)

def predictsinglefile(model, filepath):
    filepath = os.path.abspath(filepath)
    assert os.path.isfile(filepath), "File " + str(filepath) + " does not exist"
    outputpath = os.path.dirname(filepath) + "/" + os.path.splitext(os.path.basename(filepath))[0] + "_hinted.png"
    original = io.imread(filepath)
    hinted = predict(model, original)
    io.imsave(outputpath, hinted)

def predicticonset(model, filepath):
    filepath = os.path.abspath(filepath)
    # Make sure file exists
    assert os.path.isfile(filepath), "File " + str(filepath) + " does not exist"

    # Set up iconset folder
    outputpath = os.path.dirname(filepath) + "/" + os.path.splitext(os.path.basename(filepath))[0] + ".iconset/"
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)

    # List of sizes to make (lowest to highest)
    sizes = [(1024, ["icon_512x512@2x"]),
             (512,  ["icon_512x512", "icon_256x256@2x"]),
             (256,  ["icon_256x256", "icon_128x128@2x"]),
             (128,  ["icon_128x128"]),
             (64,   ["icon_32x32@2x"]),
             (32,   ["icon_32x32", "icon_16x16@2x"]),
             (16,   ["icon_16x16"])
            ]
    sizes.reverse()

    # Read the given image
    current = io.imread(filepath)

    # Convert it to all of the sizes in decreasing order
    while (sizes):
        currentsize = len(current)
        while (currentsize < sizes[-1][0]):
            sizes.pop()
        targetsizeandnames = sizes.pop()
        targetsize = targetsizeandnames[0]
        targetnames = targetsizeandnames[1]
        if (currentsize != targetsize):
            current = imresize(current, targetsize)
        for name in targetnames:
            io.imsave(outputpath + name + ".png", current)
        current = predict(model, current)

# Create model
hintbot = createModel()

# Save weights to web directory if necessary
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

# Train if no files provided
if len(args.files) == 0:
    train(hintbot)
else:
    # Otherwise, predict
    for filepath in args.files:
        if args.makeiconset:
            predicticonset(hintbot, filepath)
        else:
            predictsinglefile(hintbot, filepath)


# Save results on test set to a folder
# if not os.path.exists(args.predictionfolder):
#     os.makedirs(args.predictionfolder)
# for i in range(0, len(test_predictions)):
#     filename = str(i) + ".png"
#     io.imsave(args.predictionfolder + "/" + filename, test_predictions[i])
