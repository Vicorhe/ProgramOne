import argparse
import cv2 as cv
from glob import glob


CROPPED_SET_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/cropped/*.BMP'
DESTINATION_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/%s/%s.BMP'
NUMBER_CHUNKS = 10
SIZE = 50


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True,
                help='studio set')
ap.add_argument('-d', '--destination', required=True,
                help='destination folder')
args = vars(ap.parse_args())
studio_set = args['set']
destination_folder = args['destination']


for path in sorted(glob(CROPPED_SET_PATH % studio_set)):
    image_name = path.split('/')[-1].split('.')[0]

    img = cv.imread(path)
    img_quadrants = (('W', img[:500, :500]),
                     ('X', img[:500, 500:]),
                     ('Y', img[500:, :500]),
                     ('Z', img[500:, 500:]))

    for quadrant, quadrant_img in img_quadrants:
        for x in range(NUMBER_CHUNKS):
            for y in range(NUMBER_CHUNKS):
                tl_x, tl_y = x * SIZE, y * SIZE
                count = str(x * NUMBER_CHUNKS + y)
                sample_name = image_name + '_' + quadrant + '_' + count
                sample_name = DESTINATION_PATH % (studio_set, destination_folder, sample_name)
                cv.imwrite(sample_name, quadrant_img[tl_x:tl_x + SIZE, tl_y:tl_y + SIZE])
