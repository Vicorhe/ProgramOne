import argparse
import cv2 as cv
import numpy as np
from glob import glob
from sklearn.model_selection import StratifiedShuffleSplit
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b

SET_PATH = 'C:\\Users\\van32\\Documents\\ProgramOne\\GUI\\TrainingBatches\\one\\batch_2\\*.BMP'
LABELS_PATH = 'C:\\Users\\van32\\Documents\\ProgramOne\\GUI\\TrainingBatches\\one\\batch_2\\labels.txt'


def get_data():
    set_of_paths = sorted(glob(SET_PATH))
    data_container = list()
    for path in set_of_paths:
        image = cv.imread(path)
        converted_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        data_container.append(feature_set_a(converted_image, ('H', 'S', 'V')))
    stacked_data = np.vstack(data_container)
    labels = None
    with open(LABELS_PATH) as labels_file:
        for line in labels_file:
            labels = np.array(line.split())
    # split training and testing set
    n_splits = 1
    test_set_size = 0.25
    random_state = 6117
    sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size,
                                 random_state=random_state)
    train_index, test_index = next(sss.split(stacked_data, labels))
    training_data, training_labels = np.array([stacked_data[train_index]]), labels[train_index]
    testing_data, testing_labels = np.array([stacked_data[test_index]]), labels[test_index]
    return training_data, testing_data, training_labels, testing_labels


