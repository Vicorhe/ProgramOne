import argparse
import cv2 as cv
import numpy as np
from glob import glob
from sklearn.model_selection import StratifiedShuffleSplit
from .FeatureExtraction.feature_set_a import get_statistics as feature_set_a
from .FeatureExtraction.feature_set_b import get_statistics as feature_set_b


IMAGE_SET_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/*.BMP'
LABELS_FILE_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/labels.txt'
TEST_IMAGE_SET_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/test/*.BMP'
TEST_LABELS_FILE_PATH = '/Users/victorhe/Pictures/tileDataSet/%s/test/labels.txt'
OPTIONS = {'rgb': (cv.COLOR_BGR2RGB, ('R', 'G', 'B')),
           'hsv': (cv.COLOR_BGR2HSV, ('H', 'S', 'V')),
           'lab': (cv.COLOR_BGR2LAB, ('L', 'A', 'B')),
           'ycrcb': (cv.COLOR_BGR2YCR_CB, ('Y', 'Cr', 'Cb'))}


def get_raw_data_set():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--set',
                    required=True,
                    help='set of images being evaluated')
    ap.add_argument('-f', '--feature-set',
                    default='a',
                    help='which feature set to use',
                    choices=['a', 'b'])
    ap.add_argument('-c', '--color-space',
                    default='hsv',
                    help='color space option to evaluate',
                    choices=['rgb', 'hsv', 'lab', 'ycrcb'])
    ap.add_argument('-m', '--manual',
                    help='whether or not to perform manual splitting of '
                         + 'training and testing sets',
                    action='store_true')
    args = vars(ap.parse_args())

    set_param = args['set']
    color_space, channels = OPTIONS[args['color-space']]
    print(channels)

    image_set, test_image_set, y, test_y = list(), list(), list(), list()

    for path in sorted(glob(IMAGE_SET_PATH % set_param)):
        image_label = path.split('/')[-1].split('.')[0]
        converted_image = cv.cvtColor(cv.imread(path), color_space)
        image_set.append((converted_image, image_label))

    with open(LABELS_FILE_PATH % set_param) as f:
        for line in f:
            y = np.array(line.split())

    if args['m']:
        for path in sorted(glob(TEST_IMAGE_SET_PATH % set_param)):
            image_label = path.split('/')[-1].split('.')[0]
            converted_image = cv.cvtColor(cv.imread(path), color_space)
            test_image_set.append((converted_image, image_label))

        with open(TEST_LABELS_FILE_PATH % set_param) as f:
            for line in f:
                test_y = np.array(line.split())

    return image_set, y, channels, test_image_set, test_y


get_raw_data_set()

def load_tile_data_set():
    # fetch the raw image set and labels
    image_set, y, channels, test_image_set, test_y = get_raw_data_set()

    manual = len(test_image_set) != 0 and len(test_y) != 0

    if not manual:
        # generate feature matrix from image set
        X = np.vstack([feature_func(img, channels) for img, _ in image_set])

        # split training and testing set
        n_splits = 1
        test_set_size = 0.3
        random_state = 6117
        sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size, random_state=random_state)
        train_index, test_index = next(sss.split(X, y))
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

    else:
        X_train = np.vstack([feature_func(img, channels) for img, _ in image_set])
        y_train = y
        X_test = np.vstack([feature_func(img, channels) for img, _ in test_image_set])
        y_test = test_y

    # avoid data copy
    assert X_train.flags['C_CONTIGUOUS']
    assert X_test.flags['C_CONTIGUOUS']
    assert y_train.flags['C_CONTIGUOUS']
    assert y_test.flags['C_CONTIGUOUS']

    return X_train, y_train, X_test, y_test
