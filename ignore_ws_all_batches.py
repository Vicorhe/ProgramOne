import cv2 as cv
import numpy as np
from pathlib import Path
from sys import platform
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b
from Utilities.utils import unison_shuffled_copies


MAC_PICTURES_PATH = '/Users/victorhe/Pictures'
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures'


BATCHES = ['batch_1', 'batch_3', 'batch_4', 'batch_5', 'batch_6', 'batch_7', 'batch_8']


def process_data():
    data_container = list()
    labels = list()
    for batch in BATCHES:

        base_path = MAC_PICTURES_PATH if platform == "darwin" else WINDOWS_PICTURES_PATH
        image_base_path = Path(base_path) / batch
        image_paths = sorted(image_base_path.glob('*.BMP'))
        labels_path = Path(base_path) / batch / 'labels.txt'

        for path in image_paths:
            image = cv.imread(str(path))
            i_1 = image[152:655, :]
            i_2 = image[725:, :]
            image_3 = np.concatenate((i_1, i_2), axis=0)
            converted_image = cv.cvtColor(image_3, cv.COLOR_BGR2HSV)
            data_container.append(feature_set_a(converted_image, ('H', 'S', 'V')))

        with open(labels_path) as labels_file:
            for line in labels_file:
                labels.extend(line.split())

    labels = np.array(labels)

    stacked_data = np.vstack(data_container)
    sorted_indices = np.argsort(labels)

    sorted_data = stacked_data[sorted_indices]
    sorted_labels = labels[sorted_indices].reshape((-1, 1))
    processed_labels = np.extract(sorted_labels < '3', sorted_labels)

    first_how_many = len(processed_labels)
    processed_data = sorted_data[:first_how_many]

    training_data, training_labels = unison_shuffled_copies(processed_data, processed_labels)

    return training_data, training_labels.ravel()


process_data()