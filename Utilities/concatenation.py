import argparse
from glob import glob
import cv2 as cv
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
ap.add_argument('-n', '--name', required=True, help='name of output file')
args = vars(ap.parse_args())
image_set = list()
for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*.jpeg' % args['set'])):
    img = cv.imread(path)
    image_set.append(img)

result_image = np.concatenate(image_set)

filename = '/Users/victorhe/Pictures/colorQuantization/%s/%s_color_range.jpeg' % (args['set'], args['name'])
print(filename)
#cv.imwrite(filename, result_image)
