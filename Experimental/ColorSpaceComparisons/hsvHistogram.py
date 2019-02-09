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
    for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*.BMP' % set_param)):
        img = cv.imread(path)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        image_set.append((hsv, path.split('/')[-1]))
    return image_set


def plot_image_set(image_set):
    set_size = len(image_set)
    for i, (image, name) in enumerate(image_set):
        rgb = cv.cvtColor(image, cv.COLOR_HSV2RGB)
        plt.subplot(set_size, 2, 2*i+1), plt.imshow(rgb)
        plt.title(name), plt.xticks([]), plt.yticks([])

        plt.subplot(set_size, 2, 2*i+2), plot_hsv_histogram(image)
        plt.title('hist_' + str(i + 1)), plt.xticks([]), plt.yticks([])
    plt.show()


def plot_hsv_histogram(image):
    hist_hue = cv.calcHist([image], [0], None, [180], [0, 180])
    hist_saturation = cv.calcHist([image], [1], None, [256], [0, 256])
    hist_value = cv.calcHist([image], [2], None, [256], [0, 256])
    plt.plot(hist_hue, color='y')
    plt.plot(hist_saturation, color='b')
    plt.plot(hist_value, color='g')
    plt.xlim([0, 256])


plot_image_set(get_image_set())
