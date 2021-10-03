
#------------------------------------------------------------------------#
#  Author: Miles Winter                                                  #
#  Date: 07-14-2017                                                      #
#  Project: DECO                                                         #
#  Desc: zoom in on brightest pixel and classify blobs with CNN          #
#  Note: Need the following installed:                                   #
#        $ pip install --user --upgrade h5py theano keras                #
#        Change keras backend to theano (default is tensorflow)          #
#        Importing keras generates a .json config file                   #
#        $ KERAS_BACKEND=theano python -c "from keras import backend"    #
#        Next, to change "backend": "tensorflow" -> "theano" type        #
#        $ sed -i 's/tensorflow/theano/g' $HOME/.keras/keras.json        #
#        Documentation at https://keras.io/backend/                      #
#------------------------------------------------------------------------#


import os
import numpy as np
import pandas as pd
import keras
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Cropping2D
from keras.layers import Flatten, Dense, Dropout
from keras.layers.advanced_activations import LeakyReLU
from PIL import Image
from collections import defaultdict


def build_model(n_classes, training=False):
    """Define model structure"""
    model = Sequential()

    if training:
        model.add(Cropping2D(cropping=18,input_shape=(64, 64, 1)))
        model.add(Conv2D(64, (3, 3), padding='same'))
    else:
        model.add(Conv2D(64, (3, 3), padding='same', input_shape=(64, 64, 1)))

    model.add(LeakyReLU(alpha=0.3))
    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(Conv2D(256, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(512, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(Conv2D(512, (3, 3), padding='same'))
    model.add(LeakyReLU(alpha=0.3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=0.3))
    model.add(Dropout(0.5))
    model.add(Dense(2048))
    model.add(LeakyReLU(alpha=0.3))
    model.add(Dropout(0.5))
    model.add(Dense(n_classes, activation='softmax'))
    return model

def get_event_id(path):
    """Return the event ID for a given image file."""
    directory, filename = os.path.split(path)
    event_id, ext = os.path.splitext(filename)
    return event_id


def get_predicted_label(probs, track_thresh):
    """Returns predicted label. Track if prediction is > track_thresh """
    if probs[-1] >= track_thresh:
        return 'Track'
    else:
        return 'Other'


def get_crop_range(maxX, maxY, size=32):
    """define region of image to crop"""
    return maxX - size, maxX + size, maxY - size, maxY + size


def pass_edge_check(maxX, maxY, img_shape, crop_size=64):
    """checks if image is on the edge of the sensor"""
    x0, x1, y0, y1 = get_crop_range(maxX, maxY, size=crop_size / 2)
    checks = np.array([x0 >= 0, x1 <= img_shape[0], y0 >= 0, y1 <= img_shape[1]])
    return checks.all() == True


def convert_image(img, dims=64, channels=1):
    """convert image to grayscale, normalize, and reshape"""
    img = np.array(img, dtype='float32')
    gray_norm_img = np.mean(img, axis=-1)
    return gray_norm_img.reshape(1, dims, dims, channels)


def get_brightest_pixel(img):
    """get brightest image pixel indices"""
    img = np.array(img)
    #print(img.max())
    return np.unravel_index(img.argmax(), img.shape)


def run_blob_classifier(paths, n_classes, track_thresh=0.8,
                        weights_file='/data/user/mrmeehan/deco/classification/cnn/final_trained_weights.h5'):
    """Classify blobs with CNN"""
    # Build CNN model and load weights
    try:
        model = build_model(n_classes)
        model.load_weights(weights_file)
    except IOError:
        print('Weights could not be found ... check path')
        raise SystemExit

    class_labels = ['worm', 'spot', 'track', 'noise']
    data = defaultdict(list)

    file_counter = 0

    for filename in paths:
        
        print("reading " + str(file_counter) + " out of " + str(len(paths)))
        file_counter += 1
        
        f_reader = open(filename, 'r')
        image = []
        while 1:
            temp = f_reader.readline().split()
            temp_hold = []
            if len(temp) < 1:
                break

            for content in temp:
                temp_hold.append(float(content))

            image.append(temp_hold)

        image = np.array(image)

        # Find the brightest pixel

        predicted_label = ''
        probability = 0.
        # Check if blob is near sensor edge


        # Convert to grayscale, normalize, and reshape

        gray_image = (np.array(image, dtype='float32')/255).reshape(1, 64, 64, 1)


        # Predict image classification
        probability = model.predict(gray_image, batch_size=1, verbose=0)
        probability = probability.reshape(n_classes,)

        # Convert prediction probability to a single label
        #predicted_label = get_predicted_label(probability, track_thresh)


        # Add predicted class label and probabilities from model
        for idx, class_label in enumerate(class_labels):
            data['p_{}'.format(class_label)].append(probability[idx])

        data['image_file'].append(filename)
        event_id = get_event_id(filename)
        data['event_id'].append(event_id)

    df_data = pd.DataFrame.from_records(data)
    
    return df_data
