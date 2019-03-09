import argparse
from random import randint
import cv2 as cv


DIMENSION = 150
GRANULARITY = 30
RANDOM_LIMIT = (1000 - DIMENSION) // GRANULARITY

source_path = '/Users/victorhe/Pictures/studioSourceTiles/SS5/cropped/%s.BMP'
destination_path = '/Users/victorhe/Pictures/studioSourceTiles/SS5/%s/%s_%d.BMP'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True,
                help='set of images being evaluated')
ap.add_argument('-i', '--image', required=True,
                help='image to be split')
ap.add_argument('-n', '--number', default=200, type=int,
                help='number of samples to generate')
args = vars(ap.parse_args())
image_set = list()

source_path = source_path % (args['image'])
print(source_path)

unique_samples = set()
img = cv.imread(source_path)


for i in range(args['number']):
    tl_x = randint(0, RANDOM_LIMIT) * GRANULARITY
    tl_y = randint(0, RANDOM_LIMIT) * GRANULARITY
    unique_samples.add((tl_x, tl_y))
    destination = destination_path % (args['set'], args['set'], i)
    cv.imwrite(destination, img[tl_x: tl_x + DIMENSION, tl_y: tl_y + DIMENSION])

print('uniqueness ratio: %.3f' % (len(unique_samples)/args['number']))
