import argparse
from glob import glob
import cv2 as cv
import numpy as np
from sklearn import svm
from Utilities.utils import unison_shuffled_copies

from sklearn.model_selection import train_test_split


training_set_path = '/Users/victorhe/Pictures/colorQuantization/%s/*.BMP'
testing_set_path = '/Users/victorhe/Pictures/colorQuantization/%s/test/*.BMP'

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


training_set = list()
testing_set = list()

# get all color converted training images
for path in sorted(glob(training_set_path % set_param)):
    image_label = path.split('/')[-1].split('.')[0]
    converted_image = cv.cvtColor(cv.imread(path), color_space)
    training_set.append((converted_image, image_label))

# get all color converted testing images
for path in sorted(glob(testing_set_path % set_param)):
    image_label = path.split('/')[-1].split('.')[0]
    converted_image = cv.cvtColor(cv.imread(path), color_space)
    testing_set.append((converted_image, image_label))


def get_statistics(image):
    stats = list()
    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        # print('%s mean: %f' % (channel, np.mean(current_channel)), end=' ')
        # print('%s vari: %f' % (channel, np.var(current_channel)), end=' ')

        stats.append(np.mean(current_channel))
        stats.append(np.var(current_channel))
    # print()
    return np.array(stats)


X_train = np.vstack([get_statistics(img) for img, _ in training_set])

X_test = np.vstack([get_statistics(img) for img, _ in testing_set])

y_train = list()

y_test = list()

with open('/Users/victorhe/Pictures/colorQuantization/%s/labels.txt' % set_param) as f:
    for line in f:
        y_train = line.split()

with open('/Users/victorhe/Pictures/colorQuantization/%s/test/labels.txt' % set_param) as f:
    for line in f:
        y_test = line.split()

y_train = np.array(y_train)

y_test = np.array(y_test)

print(*X_train)
print(*y_train)

X_train, y_train = unison_shuffled_copies(X_train, y_train)

print(*X_train)
print(*y_train)

# X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=5, shuffle=True, stratify=y)


def SVM_SVC(X, y, c):
    for k in ['linear', 'poly', 'rbf', 'sigmoid']:
        clf = svm.SVC(kernel=k, C=c, gamma='scale')
        clf.fit(X_train, y_train)
        print('training set score:', clf.score(X_train, y_train))
        print('testing set score:', clf.score(X_test, y_test))
        print()
    return


for c in [0.1, 1, 10]:
    SVM_SVC(X_test, y_test, c)




