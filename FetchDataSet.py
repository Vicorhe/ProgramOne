import cv2 as cv
import numpy as np
from pathlib import Path
from sys import platform
from sklearn.model_selection import StratifiedShuffleSplit
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b
from Utilities.utils import unison_shuffled_copies


MAC_PICTURES_PATH = '/Users/victorhe/Pictures'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures'


BATCH_NAME = 'batch_1'


def load_tile_data_set():
    image_paths = sorted(get_base_path().glob('*.BMP'))
    labels_path = get_base_path() / 'labels.txt'

    data_container = list()
    for path in image_paths:
        image = cv.imread(str(path))
        # [start_row:end_row, start_col:end_col]
        i_1 = image[152:655, :]
        i_2 = image[725:, :]
        # stack two cropped images vertically
        image_3 = np.concatenate((i_1, i_2), axis=0)
        converted_image = cv.cvtColor(image_3, cv.COLOR_BGR2HSV)
        data_container.append(feature_set_a(converted_image, ('H', 'S', 'V')))
    stacked_data = np.vstack(data_container)

    labels = None
    with open(labels_path) as labels_file:
        for line in labels_file:
            labels = np.array(line.split())

    training_data, training_labels = unison_shuffled_copies(stacked_data, labels)

    # avoid data copy
    assert training_data.flags['C_CONTIGUOUS']
    assert training_labels.flags['C_CONTIGUOUS']

    return training_data, training_labels


def get_base_path():
    base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
    return Path(base_path) / BATCH_NAME
