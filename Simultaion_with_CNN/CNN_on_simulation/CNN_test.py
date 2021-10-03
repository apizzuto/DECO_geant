import json
from PIL import Image
import argparse
import os
import h5py
import zoom_predictions_4class
import numpy as np
import pandas as pd
import decotools as dt
from zoom_predictions_4class import run_blob_classifier
from shutil import copy2



# CNN class probability thresholds
# Event is classified as 'key' if CNN prob is > value, otherwise 'ambiguous'
class_thresholds = {'track': 0.8,
                    'worm': 0.8,
                    'spot': 0.8,
                    'noise': 0.8
                    }

def get_predicted_label(event, thresholds=class_thresholds):
    """Return predicted label for an event.

    Parameters
    ----------
    event : pandas.Series
        Row of dataframe containing event id, image path, centroid coordinates,
        and CNN class probabilities
    thresholds : dict
        Dictionary containing cutoff threshold for each class probability
        e.g., 'track' : 0.8

    Returns
    -------
    pred : str
        Predicted event classification label
    """

    if event['p_track'] < 0:
        pred = 'Edge'
    elif event['p_noise'] > thresholds['noise']:
        pred = 'Noise'
    elif event['p_spot'] > thresholds['spot']:
        pred = 'Spot'
    elif event['p_track'] > thresholds['track']:
        pred = 'Track'
    elif event['p_worm'] > thresholds['worm']:
        pred = 'Worm'
    else:
        pred = 'Ambiguous'

    return pred


def get_events():

    # Replace extension with the jpg extension of the raw, i.e. unprocessed, event image
    absolute_paths = []


    base = '../MC_Simulation/output/' + file_dir + '/' + source_dir + '/'

    for filename in os.listdir(base):
        if filename.endswith(".txt"):
            absolute_paths.append(base + filename)

    return absolute_paths

file_dir = "qdc_res_0_smear_0_slope_7"

source_dir = 'mu+_2Dimages_fac1.5_dev0_condev0'

if __name__ == '__main__':

    cnn_weights_file = './final_trained_weights.h5'

    # Get all paths
    paths = get_events()
    print(paths)
    # Use args.index and args.n_images for batch processing
    df = run_blob_classifier(paths, 4,
                             weights_file=cnn_weights_file)

    if not os.path.exists("./classification"):
        os.mkdir("./classification")

    if not os.path.exists("./classification/" + file_dir):
        os.mkdir("./classification/" + file_dir)

    if not os.path.exists("./classification/" + file_dir + '/' + source_dir):
        os.mkdir("./classification/" + file_dir + '/' + source_dir)

    total_num = 0
    track_num = 0

    for i in range(len(df["p_track"])):

        total_num += 1

        if df["p_track"][i] > 0.5:
            track_num += 1

            if not os.path.exists("./classification/" + file_dir + '/' + source_dir +  "/track"):
                os.mkdir("./classification/" + file_dir + '/' + source_dir + "/track")

            copy2(paths[i], "./classification/" + file_dir + '/' + source_dir +  "/track/")

        if df["p_worm"][i] > 0.5:

            if not os.path.exists("./classification/" + file_dir + '/' + source_dir +  "/worm"):
                os.mkdir("./classification/" + file_dir + '/' + source_dir + "/worm")

            copy2(paths[i], "./classification/" + file_dir + '/' + source_dir +  "/worm/")

        if df["p_spot"][i] > 0.5:

            if not os.path.exists("./classification/" + file_dir + '/' + source_dir +  "/spot"):
                os.mkdir("./classification/" + file_dir + '/' + source_dir + "/spot")

            copy2(paths[i], "./classification/" + file_dir + '/' + source_dir +  "/spot/")


    print("track rate " + str(float(track_num)/total_num))








