import argparse
import cv2 as cv
import numpy as np
from pathlib import Path
from sys import platform
from sklearn.model_selection import StratifiedShuffleSplit
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b


MAC_PICTURES_PATH = '/Users/victorhe/Pictures'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures'


BATCH_NAME = 'batch_2'


def load_tile_data_set():
    image_paths = sorted(get_base_path().glob('*.BMP'))
    labels_path = get_base_path() / 'labels.txt'

    data_container = list()
    for path in image_paths:
        image = cv.imread(str(path))
        converted_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        data_container.append(feature_set_a(converted_image, ('H', 'S', 'V')))
    stacked_data = np.vstack(data_container)

    labels = None
    with open(labels_path) as labels_file:
        for line in labels_file:
            labels = np.array(line.split())

    # split training and testing set
    n_splits = 1
    test_set_size = 0.25
    sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size)
    train_index, test_index = next(sss.split(stacked_data, labels))

    training_data, training_labels = np.array([stacked_data[train_index]]), labels[train_index]
    testing_data, testing_labels = np.array([stacked_data[test_index]]), labels[test_index]

    # avoid data copy
    assert training_data.flags['C_CONTIGUOUS']
    assert testing_data.flags['C_CONTIGUOUS']
    assert training_labels.flags['C_CONTIGUOUS']
    assert testing_labels.flags['C_CONTIGUOUS']

    return training_data, testing_data, training_labels, testing_labels


def get_base_path():
    base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
    return Path(base_path) / BATCH_NAME
