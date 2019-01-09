import argparse
from glob import glob
import cv2 as cv
from matplotlib import pyplot as plt

options = {'rgb': (cv.COLOR_BGR2RGB, ),
           'hsv': (cv.COLOR_BGR2HSV, ),
           'lab': (cv.COLOR_BGR2LAB, ),
           'ycrcb': (cv.COLOR_BGR2YCR_CB, ),
           'gray': (cv.COLOR_BGR2GRAY, 1)}

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--option', required=True, help='color space option to evaluate, choices: rgb, hsv, lab, ycrcb, gray')
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())
set_param = args['set']
image_set = list()

for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*' % set_param)):
    image_set.append((cv.imread(path, 0), path.split('/')[-1]))




def plot_image_set(image_set):
    set_size = len(image_set)
    for i, (image, name) in enumerate(image_set):
        plt.subplot(set_size, 2, 2*i+1), plt.imshow(image, cmap='gray')
        plt.title(name), plt.xticks([]), plt.yticks([])

        plt.subplot(set_size, 2, 2*i+2), plot_histogram(image)
        plt.title('hist_' + str(i + 1)), plt.xticks([]), plt.yticks([])

    plt.show()


def plot_histogram(image):
    hist = cv.calcHist([image], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.xlim([0, 256])
