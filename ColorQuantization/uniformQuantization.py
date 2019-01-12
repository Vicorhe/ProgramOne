import argparse
from glob import glob
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def image_set_stats(image_set):
    top_k, features = [], []
    for img in image_set:
        hist = get_quantized_histogram(img)
        top_k_colors = get_top_k_values(hist, 3)
        top_k.append(top_k_colors)
        features.append(get_color_features(top_k_colors))
    return top_k, features


def plot_image_set_vertical(image_set):
    set_size = len(image_set)
    i = 0
    for img in image_set:
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hist = get_quantized_histogram(img)
        plt.subplot(set_size, 2, 2 * i + 1), plt.imshow(rgb), plt.title('img_' + str(i + 1)), plt.xticks([]), plt.yticks([])
        plt.subplot(set_size, 2, 2 * i + 2), plt.plot(hist), plt.title('hist_' + str(i + 1)), plt.xticks([]), plt.yticks([])
        i += 1

    plt.show()


def plot_image_set_horizontal(image_set):
    set_size = len(image_set)
    i = 1
    for img in image_set:
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hist = get_quantized_histogram(img)
        plt.subplot(2, set_size, i), plt.imshow(rgb), plt.title('img_' + str(i)), plt.xticks([]), plt.yticks([])
        plt.subplot(2, set_size, set_size + i), plt.plot(hist), plt.title('hist_' + str(i)), plt.xticks([]), plt.yticks([])
        i += 1

    plt.show()


def compare_image_set(image_set):
    stats = image_set_stats(image_set)
    for t, f in zip(*stats):
        print(t, f)
    plot_image_set_vertical(image_set)
    # plot_image_set_horizontal(image_set)


def get_quantized_histogram(img):
    hsv = cv.cvtColor(img[0], cv.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    quantized_img = np.zeros((h, w), np.uint8)

    for row in range(h):
        for col in range(w):
            quantized_img[row, col] = pixel_quantization(hsv[row, col])

    hist = cv.calcHist([quantized_img], [0], None, [72], [0, 71])
    return hist


def pixel_quantization(pixel):
    h, s, v = pixel
    return 9 * get_hue_quantity(h) + 3 * get_percentage_quantity(s) + get_percentage_quantity(v)


def get_hue_quantity(val):
    if val >= 158 or val <= 10:
        return 0
    elif val <= 20:
        return 1
    elif val <= 37:
        return 2
    elif val <= 77:
        return 3
    elif val <= 95:
        return 4
    elif val <= 135:
        return 5
    elif val <= 147:
        return 6
    else:
        return 7


def get_percentage_quantity(val):
    percentage = val/255
    if percentage < 0.2:
        return 0
    elif percentage < 0.7:
        return 1
    else:
        return 2


def get_top_k_values(hist, k):
    hist = enumerate(hist.ravel())
    ordered_hist = sorted(hist, key=lambda x: x[1], reverse=True)
    top_k_values = [v for v, q in ordered_hist[:k]]
    return  top_k_values


def get_color_features(top_colors):
    return np.average(top_colors), np.std(top_colors)


def get_image_set():
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
    args = vars(ap.parse_args())
    set_param = args['set']
    image_set = list()
    for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*' % set_param)):
        img = cv.imread(path)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        image_set.append((hsv, path.split('/')[-1]))
    return image_set


compare_image_set(get_image_set())





