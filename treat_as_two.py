import cv2 as cv
import numpy as np
from pathlib import Path
from sys import platform
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b
from Utilities.utils import unison_shuffled_copies


MAC_PICTURES_PATH = '/Users/victorhe/Pictures'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures'


BATCH_NAME = 'batch_8'


def process_data():
    image_paths = sorted(get_base_path().glob('*.BMP'))
    labels_path = get_base_path() / 'labels.txt'

    data_container = list()
    for path in image_paths:
        image = cv.imread(str(path))
        i_1 = image[152:655, :]
        i_2 = image[725:, :]
        image_3 = np.concatenate((i_1, i_2), axis=0)
        converted_image = cv.cvtColor(image_3, cv.COLOR_BGR2HSV)
        data_container.append(feature_set_a(converted_image, ('H', 'S', 'V')))
    stacked_data = np.vstack(data_container)

    labels = None
    with open(labels_path) as labels_file:
        for line in labels_file:
            labels = np.array(line.split())

    sorted_indices = np.argsort(labels)

    sorted_data = stacked_data[sorted_indices]
    sorted_labels = labels[sorted_indices].reshape((-1, 1))
    sorted_labels = np.where(sorted_labels == '3', '2', sorted_labels)
    sorted_labels = np.where(sorted_labels == '4', '2', sorted_labels)

    training_data, training_labels = unison_shuffled_copies(sorted_data, sorted_labels)

    return training_data, training_labels.ravel()


def get_base_path():
    base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
    return Path(base_path) / BATCH_NAME
