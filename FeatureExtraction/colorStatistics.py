import argparse
from glob import glob
import cv2 as cv
from matplotlib import pyplot as plt

options = {'rgb': (cv.COLOR_BGR2RGB, ('red', 'green', 'blue')),
           'hsv': (cv.COLOR_BGR2HSV, ('hue', 'saturation', 'value')),
           'lab': (cv.COLOR_BGR2LAB, ('luminance', 'a component', 'b component')),
           'ycrcb': (cv.COLOR_BGR2YCR_CB, ('y component', 'Cr', 'Cb')),
           'gray': (cv.COLOR_BGR2GRAY, ('value'))}

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--option', required=True, help='color space option to evaluate, choices: rgb, hsv, lab, ycrcb, gray')
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())

set_param = args['set']
color_space, dimensions = options[args['option']]

print(color_space)

image_set = list()

# get all color space converted images and their corresponding labels
for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*' % set_param)):
    image_label = path.split('/')[-1].split('.')[0]
    image = cv.cvtColor(cv.imread(path), color_space)
    image_set.append((image, image_label))

print(image_set)

#def get_statistics(hist):
#    return

def plot_histogram(image):
    hist = cv.calcHist([image], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.xlim([0, 256])


