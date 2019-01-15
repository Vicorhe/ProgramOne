import argparse
from glob import glob
import cv2 as cv
import numpy as np


set_path_expression = '/Users/victorhe/Pictures/colorQuantization/%s/*.BMP'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())

set_param = args['set']

image_set = list()

# get all color space converted images and their corresponding labels
for path in sorted(glob(set_path_expression % set_param)):
    image_label = path.split('/')[-1].split('.')[0]
    image = cv.imread(path)
    image_set.append((image, image_label))
