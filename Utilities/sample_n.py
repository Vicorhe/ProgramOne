import argparse
from random import randint
import cv2 as cv
from glob import glob

CROPPED_SET_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/cropped/*.BMP'

SOURCE_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/cropped/%s.BMP'

DESTINATION_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/%s/%s.BMP'


NUM_SAMPLES = 30
DIMENSION = 50
GRANULARITY = 30
RANDOM_LIMIT = (500 - DIMENSION) // GRANULARITY


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True,
                help='studio set')
ap.add_argument('-d', '--destination', required=True,
                help='destination folder')
args = vars(ap.parse_args())
studio_set = args['set']
destination_folder = args['destination']

image_set = list()


for path in sorted(glob(CROPPED_SET_PATH % studio_set)):
    image_name = path.split('/')[-1].split('.')[0]
    source_image_path = SOURCE_PATH % (studio_set, image_name)

    img = cv.imread(source_image_path)
    img_quadrants = (('W', img[:500, :500]),
                     ('X', img[:500, 500:]),
                     ('Y', img[500:, :500]),
                     ('Z', img[500:, 500:]))

    for quadrant, quadrant_img in img_quadrants:
        unique_samples = set()
        for i in range(NUM_SAMPLES):
            tl_x = randint(0, RANDOM_LIMIT) * GRANULARITY
            tl_y = randint(0, RANDOM_LIMIT) * GRANULARITY
            unique_samples.add((tl_x, tl_y))
            sample_name = image_name + '_' + str(i) + '_' + quadrant
            destination_path = DESTINATION_PATH % (studio_set, destination_folder, sample_name)
            cv.imwrite(destination_path, quadrant_img[tl_x: tl_x + DIMENSION, tl_y: tl_y + DIMENSION])
        print('uniqueness ratio: %.3f' % (len(unique_samples)/NUM_SAMPLES))
