import cv2 as cv
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
from sys import platform
from FeatureExtraction.feature_set_a import get_statistics, get_feature_names


WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures\\TrainingBatches\\three'


def images_to_data_frame(batch_name):
    """
    ONLY USE on WINDOWS WORKSTATION

    This method is meant to be called once to process a batch of images
    with a set roi (adjustable in get_roi()) and with a set feature_set
    (adjustable inside extract_features_from_images() and importing the
    intended feature set).

    After processing, it saves the dataFrame to the 'DataFrames' Folder
    in this project.
    """
    if platform == "darwin":
        raise OSError('This function should only be called on Windows OS.')
    feature_matrix = extract_features_from_images(batch_name)
    labels_vector = read_labels_into_vector(batch_name)
    df = construct_training_data_frame(feature_matrix, labels_vector)
    pickle_data_frame(batch_name, df)


def extract_features_from_images(batch_name):
    """
    Constructs feature matrix out of a batch of images.
    """
    image_paths = sorted(get_batch_source_path(batch_name).glob('*.BMP'))
    feature_vectors = list()
    for path in image_paths:
        image = cv.imread(str(path))
        roi = get_roi(image)
        converted_image = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        feature_vectors.append(get_statistics(converted_image))
    feature_matrix = np.vstack(feature_vectors)
    return feature_matrix


def get_batch_source_path(batch_name):
    return Path(WINDOWS_PICTURES_PATH) / batch_name


def get_roi(image):
    """
    Specify which region within the source image to use.
    reminder on how to interpret numpy array cropping:
        [start_row:end_row, start_col:end_col]
    """
    roi = image[60:940, 260:1140]
    return roi


def read_labels_into_vector(batch_name):
    """
    Read 'labels.txt' file and puts it into a vector
    """
    labels_path = get_batch_source_path(batch_name) / 'labels.txt'
    labels_vector = None
    with open(labels_path) as labels_file:
        for line in labels_file:
            labels_from_file = line.split()
            # converts any label besides '1' and '2' to '5'
            labels_from_file = list(map(lambda x: '5' if x > '2' else x, labels_from_file))
            labels_vector = np.array(labels_from_file).reshape((-1, 1))
    return labels_vector


def construct_training_data_frame(feature_matrix, labels_vector):
    """
    Stacks features and labels to form a DataFrame
    """
    data = np.hstack((feature_matrix, labels_vector))
    columns = get_feature_names()
    columns.append('Labels')
    df = pd.DataFrame(data, columns=columns)
    return df


def pickle_data_frame(batch_name, df):
    """
    Create pickle file of DataFrame
    """
    pickle_file_name = batch_name + '.pickle'
    pickle_file_name = get_data_frame_base_path() / pickle_file_name
    with open(pickle_file_name, 'wb') as f:
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)


def load_pickled_data_frame(batch_name):
    """
    Load DataFrame from pickle file.
    """
    pickle_file_name = batch_name + '.pickle'
    pickle_file_name = get_data_frame_base_path() / pickle_file_name
    with open(pickle_file_name, 'rb') as f:
        df = pickle.load(f)
    return df


def get_data_frame_base_path():
    return Path(os.getcwd()) / 'DataFrames'


def concatenate_data_frames(component_batch_names, combined_batch_name):
    """
    Combine component batche DataFrames into a larger aggregate DataFrame.
    """
    batch_df_s = [load_pickled_data_frame(batch_name) for batch_name in component_batch_names]
    df = pd.concat(batch_df_s, ignore_index=True)
    pickle_data_frame(combined_batch_name, df)
