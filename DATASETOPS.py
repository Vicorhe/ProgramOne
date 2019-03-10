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
CLASSIC_LABELS_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/labels.txt'



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

image_set, test_image_set, y, test_y = list(), list(), list(), list()


set_of_paths = sorted(glob(SET_PATH % img_set))

if manual:
    for test_quadrant in QUADRANTS:
        test_paths = [x for x in set_of_paths if test_quadrant in x]
        train_paths = [x for x in set_of_paths if test_quadrant not in x]


        CONTINUE HERE!!!!!!!!


else:
    # classic image round up
    for path in set_of_paths:
        image_label = path.split('/')[-1].split('.')[0]
        converted_image = cv.cvtColor(cv.imread(path), color_space)
        image_set.append((converted_image, image_label))

    with open(CLASSIC_LABELS_PATH % img_set) as f:
        for line in f:
            y = np.array(line.split())



def load_tile_data_set():

    if not manual:
        # generate feature matrix from image set
        X = np.vstack([feature_function(img, channels) for img, _ in image_set])

        # split training and testing set
        n_splits = 1
        test_set_size = 0.3
        random_state = 6117
        sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size, random_state=random_state)
        train_index, test_index = next(sss.split(X, y))
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

    else:
        X_train = np.vstack([feature_function(img, channels) for img, _ in image_set])
        y_train = y
        X_test = np.vstack([feature_function(img, channels) for img, _ in test_image_set])
        y_test = test_y

    # avoid data copy
    assert X_train.flags['C_CONTIGUOUS']
    assert X_test.flags['C_CONTIGUOUS']
    assert y_train.flags['C_CONTIGUOUS']
    assert y_test.flags['C_CONTIGUOUS']

    return X_train, y_train, X_test, y_test
