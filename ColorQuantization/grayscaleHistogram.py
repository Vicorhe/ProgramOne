import argparse
from glob import glob
import cv2 as cv
from matplotlib import pyplot as plt


def get_image_set():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
    args = vars(ap.parse_args())
    set_param = args['set']
    image_set = list()
    for path in glob('/Users/victorhe/Pictures/colorQuantization/%s/*.jpeg' % set_param):
        image_set.append((cv.imread(path, 0), path.split('/')[-1]))
    return image_set


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


plot_image_set(get_image_set())
