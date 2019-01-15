import argparse
from glob import glob
import cv2 as cv
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())


def crop_center(image):
    h, w = image.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2
    return image[mid_h - 500: mid_h + 500, mid_w - 500: mid_w + 500]


for path in sorted(glob('/Users/victorhe/Pictures/studioSourceTiles/STUDIO_SET_1/%s/*.BMP' % args['set'])):
    img = cv.imread(path)
    filename = path.split('/')[-1]
    filename_with_path = '/Users/victorhe/Pictures/studioSourceTiles/STUDIO_SET_1/%s' % filename

    result_img = crop_center(img)

    print(filename_with_path)
    cv.imwrite(filename_with_path, result_img)

