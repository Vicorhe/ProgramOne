import argparse
from glob import glob
import cv2 as cv
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())

for path in sorted(glob('/Users/victorhe/Pictures/studioSourceTiles/STUDIO_SET_1/%s/*.BMP' % args['set'])):
    img = cv.imread(path)
    filename = path.split('/')[-1]
    filename_with_path = '/Users/victorhe/Pictures/studioSourceTiles/STUDIO_SET_1/%s' % filename

    h, w = img.shape[:-1]

    mid_h = h//2
    mid_w = w//2

    result_img = img[mid_h-500:mid_h+500, mid_w-500:mid_w+500]

    print(filename_with_path)
    cv.imwrite(filename_with_path, result_img)

