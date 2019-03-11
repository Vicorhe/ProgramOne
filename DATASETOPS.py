import argparse
import cv2 as cv
import numpy as np
from glob import glob
from sklearn.model_selection import StratifiedShuffleSplit
from FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from FeatureExtraction.feature_set_b import get_statistics as feature_set_b


COLOR_SPACE_OPTIONS = {'rgb': (cv.COLOR_BGR2RGB, ('R', 'G', 'B')),
                       'hsv': (cv.COLOR_BGR2HSV, ('H', 'S', 'V')),
                       'lab': (cv.COLOR_BGR2LAB, ('L', 'A', 'B')),
                       'ycrcb': (cv.COLOR_BGR2YCR_CB, ('Y', 'Cr', 'Cb'))}
FEATURE_SPACE_OPTIONS = {'a': feature_set_a, 'b': feature_set_b}
QUADRANTS = ['W', 'X', 'Y', 'Z']
SET_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/*.BMP'
TRAIN_LABELS_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/train_labels.txt'
TEST_LABELS_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/test_labels.txt'
LABELS_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/labels.txt'


def load_tile_data_set():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--set',
                    required=True,
                    help='set of images being evaluated')
    ap.add_argument('-f', '--feature_set',
                    default='a',
                    help='which feature set to use',
                    choices=['a', 'b'])
    ap.add_argument('-c', '--color_space',
                    default='hsv',
                    help='color space option to evaluate',
                    choices=['rgb', 'hsv', 'lab', 'ycrcb'])
    ap.add_argument('-m', '--manual',
                    help='indicates to perform quadrant based splitting',
                    action='store_true')
    args = vars(ap.parse_args())
    img_set = args['set']
    feature_function = FEATURE_SPACE_OPTIONS[args['feature_set']]
    color_space, channels = COLOR_SPACE_OPTIONS[args['color_space']]
    manual = args['manual']
    set_of_paths = sorted(glob(SET_PATH % img_set))

    training_data, testing_data, training_labels, testing_labels = list(), list(), None, None

    if manual:
        for quadrant in QUADRANTS:

            train_data_container, test_data_container = list(), list()

            train_paths = [x for x in set_of_paths if quadrant not in x]
            test_paths = [x for x in set_of_paths if quadrant in x]

            # build the training data matrix
            for train_path in train_paths:
                train_image = cv.imread(train_path)
                converted_train_image = cv.cvtColor(train_image, color_space)
                train_data_container.append(feature_function(converted_train_image, channels))
            training_data.append(np.vstack(train_data_container))

            # build the testing data matrix
            for test_path in test_paths:
                test_image = cv.imread(test_path)
                converted_test_image = cv.cvtColor(test_image, color_space)
                test_data_container.append(feature_function(converted_test_image, channels))
            testing_data.append(np.vstack(test_data_container))

        training_data = np.array(training_data)
        testing_data = np.array(testing_data)

        # get training labels
        with open(TRAIN_LABELS_PATH % img_set) as train_labels_file:
            for line in train_labels_file:
                training_labels = np.array(line.split())

        # get testing labels
        with open(TEST_LABELS_PATH % img_set) as test_labels_file:
            for line in test_labels_file:
                testing_labels = np.array(line.split())

    else:
        data_container = list()
        for path in set_of_paths:
            image = cv.imread(path)
            converted_image = cv.cvtColor(image, color_space)
            data_container.append(feature_function(converted_image, channels))
        stacked_data = np.vstack(data_container)

        labels = None
        with open(LABELS_PATH % img_set) as labels_file:
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

    # avoid data copy
    assert training_data.flags['C_CONTIGUOUS']
    assert testing_data.flags['C_CONTIGUOUS']
    assert training_labels.flags['C_CONTIGUOUS']
    assert testing_labels.flags['C_CONTIGUOUS']

    return training_data, testing_data, training_labels, testing_labels
