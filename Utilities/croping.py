import argparse
import cv2 as cv
from glob import glob


SOURCE_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/*.BMP'
DESTINATION_PATH = '/Users/victorhe/Pictures/studioSourceTiles/%s/cropped/%s'


def crop_center(image):
    h, w = image.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2
    return image[mid_h - 500: mid_h + 500, mid_w - 500: mid_w + 500]


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='studio set')
args = vars(ap.parse_args())

studio_set = args['set']

for path in sorted(glob(SOURCE_PATH % studio_set)):
    img = cv.imread(path)
    filename = path.split('/')[-1]
    filename_with_path = DESTINATION_PATH % (studio_set, filename)

    result_img = crop_center(img)

    print(filename_with_path)
    cv.imwrite(filename_with_path, result_img)

