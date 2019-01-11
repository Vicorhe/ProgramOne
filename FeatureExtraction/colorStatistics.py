import argparse
from glob import glob
import cv2 as cv
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn import svm
from matplotlib import pyplot as plt

options = {'rgb': (cv.COLOR_BGR2RGB, ('R', 'G', 'B')),
           'hsv': (cv.COLOR_BGR2HSV, ('H', 'S', 'V')),
           'lab': (cv.COLOR_BGR2LAB, ('L', 'A', 'B')),
           'ycrcb': (cv.COLOR_BGR2YCR_CB, ('Y', 'Cr', 'Cb'))}

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--option', required=True, help='color space option to evaluate', choices=['rgb', 'hsv', 'lab', 'ycrcb'])
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())

set_param = args['set']
color_space, channels = options[args['option']]

image_set = list()

# get all color space converted images and their corresponding labels
for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*' % set_param)):
    image_label = path.split('/')[-1].split('.')[0]
    image = cv.cvtColor(cv.imread(path), color_space)
    image_set.append((image, image_label))


def get_statistics(image):
    stats = list()
    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]
        stats.append(np.mean(current_channel))
        stats.append(np.var(current_channel))
    return np.array(stats)


print('Feature Set: means and variance of the separate %s channels' % args['option'].upper())


X = np.vstack([get_statistics(img) for img, _ in image_set])

y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])


def SVM_SVC(X, y, c):
    for k in ['linear', 'poly','rbf', 'sigmoid']:
        clf = svm.SVC(kernel=k, C=c)
        clf.fit(X, y)
        print(clf.predict(X))
        # print(clf.score(X, y))
    return


for c in [0.1, 1, 10]:
    SVM_SVC(X, y, c)




