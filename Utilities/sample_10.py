import argparse
from random import randint
import cv2 as cv


source_path = '/Users/victorhe/Pictures/alternativeSourceTiles/%s/%s.BMP'
destination_path = '/Users/victorhe/Pictures/alternativeSourceTiles/%s/%s/%s_%d.BMP'
SAMPLE_COUNT = 10

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
ap.add_argument('-d', '--destination', required=True, help='destination directory')
ap.add_argument('-i', '--image', required=True, help='image to be split')
args = vars(ap.parse_args())
image_set = list()

source_path = source_path % (args['set'], args['image'])

img = cv.imread(source_path)

for i in range(SAMPLE_COUNT):
    tl_x, tl_y = randint(0, 19) * 30, randint(0, 19) * 30
    destination = destination_path % (args['set'], args['destination'], args['destination'], i)
    cv.imwrite(destination, img[tl_x:tl_x+300, tl_y:tl_y+300])
