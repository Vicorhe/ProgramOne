import argparse
from glob import glob
import cv2 as cv
import numpy as np


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
args = vars(ap.parse_args())
image_set = list()

for path in sorted(glob('/Users/victorhe/Pictures/colorQuantization/%s/*_.BMP' % args['set'])):
    img = cv.imread(path)
    image_set.append(img)

print('concatenating %d images' % len(image_set))

result_image = np.concatenate(image_set)

# works on BMP images

filename = '/Users/victorhe/Pictures/colorQuantization/%s/%s_training_image.BMP' % (args['set'], args['set'])

cv.imwrite(filename, result_image)
