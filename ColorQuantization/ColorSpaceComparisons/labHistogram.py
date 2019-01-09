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
    for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*' % set_param)):
        img = cv.imread(path)
        img = cv.cvtColor(img, cv.COLOR_BGR2LAB)
        image_set.append((img, path.split('/')[-1]))
    return image_set


def plot_image_set(image_set):
    set_size = len(image_set)
    for i, (image, name) in enumerate(image_set):
        rgb = cv.cvtColor(image, cv.COLOR_LAB2RGB)

        plt.subplot(set_size, 2, 2*i+1), plt.imshow(rgb)
        plt.title(name), plt.xticks([]), plt.yticks([])

        plt.subplot(set_size, 2, 2*i+2), plot_lab_histogram(image)
        plt.title('hist_' + str(i + 1)), plt.xticks([]), plt.yticks([])

    plt.show()


def plot_lab_histogram(image):
    color = ('k', 'm', 'y')
    for i, col in enumerate(color):
        hist = cv.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])


plot_image_set(get_image_set())
