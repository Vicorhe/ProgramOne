import argparse
from glob import glob
import cv2 as cv
import numpy as np


TRAINING_SET_PATH = '/Users/victorhe/Pictures/processedTileGroups/%s/*.BMP'
TESTING_SET_PATH = '/Users/victorhe/Pictures/processedTileGroups/%s/test/*.BMP'
TRAINING_LABELS_FILE_PATH = '/Users/victorhe/Pictures/processedTileGroups/%s/labels.txt'
TESTING_LABELS_FILE_PATH = '/Users/victorhe/Pictures/processedTileGroups/%s/test/labels.txt'
OPTIONS = {'rgb': (cv.COLOR_BGR2RGB, ('R', 'G', 'B')),
           'hsv': (cv.COLOR_BGR2HSV, ('H', 'S', 'V')),
           'lab': (cv.COLOR_BGR2LAB, ('L', 'A', 'B')),
           'ycrcb': (cv.COLOR_BGR2YCR_CB, ('Y', 'Cr', 'Cb'))}


def get_data_set():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o',
                    '--option',
                    default='hsv',
                    help='color space option to evaluate',
                    choices=['rgb', 'hsv', 'lab', 'ycrcb'])
    ap.add_argument('-s',
                    '--set',
                    required=True,
                    help='set of images being evaluated')
    args = vars(ap.parse_args())

    set_param = args['set']
    color_space, channels = OPTIONS[args['option']]

    training_image_set = list()
    testing_image_set = list()

    for path in sorted(glob(TRAINING_SET_PATH % set_param)):
        image_label = path.split('/')[-1].split('.')[0]
        converted_image = cv.cvtColor(cv.imread(path), color_space)
        training_image_set.append((converted_image, image_label))

    for path in sorted(glob(TESTING_SET_PATH % set_param)):
        image_label = path.split('/')[-1].split('.')[0]
        converted_image = cv.cvtColor(cv.imread(path), color_space)
        testing_image_set.append((converted_image, image_label))

    with open(TRAINING_LABELS_FILE_PATH % set_param) as f:
        for line in f:
            y_train = np.array(line.split())

    with open(TESTING_LABELS_FILE_PATH % set_param) as f:
        for line in f:
            y_test = np.array(line.split())

    return training_image_set, testing_image_set, y_train, y_test, channels


