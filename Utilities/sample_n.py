import argparse
from random import randint
import cv2 as cv


STUDIO_SET = 'SS7'
NUM_SAMPLES = 30
DIMENSION = 50
GRANULARITY = 30
RANDOM_LIMIT = (500 - DIMENSION) // GRANULARITY

source_path = '/Users/victorhe/Pictures/studioSourceTiles/%s/cropped/%s.BMP'

destination_path = '/Users/victorhe/Pictures/studioSourceTiles/%s/%s/%s/%s_%d.BMP'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True,
                help='set of images being evaluated')
ap.add_argument('-i', '--image', required=True,
                help='image to be split')
args = vars(ap.parse_args())
image_set = list()

source_path = source_path % (STUDIO_SET, args['image'])

img = cv.imread(source_path)
img_quadrants = ((img[:500, :500], 'W'),
                 (img[:500, 500:], 'X'),
                 (img[500:, :500], 'Y'),
                 (img[500:, 500:], 'Z'))

for quadrant, folder in img_quadrants:
    unique_samples = set()
    for i in range(NUM_SAMPLES):
        tl_x = randint(0, RANDOM_LIMIT) * GRANULARITY
        tl_y = randint(0, RANDOM_LIMIT) * GRANULARITY
        unique_samples.add((tl_x, tl_y))
        sample_name = args['set'] + '_' + folder
        destination = destination_path % (STUDIO_SET, args['set'], folder, sample_name, i)
        cv.imwrite(destination, img[tl_x: tl_x + DIMENSION, tl_y: tl_y + DIMENSION])
    print('uniqueness ratio: %.3f' % (len(unique_samples)/NUM_SAMPLES))
