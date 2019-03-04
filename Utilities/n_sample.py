import argparse
import cv2 as cv


source_path = '/Users/victorhe/Pictures/studioSourceTiles/STUDIO_SET_4/cropped/%s.BMP'
destination_path = '/Users/victorhe/Desktop/SS4_sampled/%s/%s_%d.BMP'

ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
ap.add_argument('-i', '--image', required=True, help='image to be split')
args = vars(ap.parse_args())
image_set = list()

source_path = source_path % (args['image'])

img = cv.imread(source_path)


tl_x, tl_y = 160, 625
destination = destination_path % (args['set'], args['set'], 0)
cv.imwrite(destination, img[tl_x:tl_x+200, tl_y:tl_y+200])

tl_x, tl_y = 260, 625
destination = destination_path % (args['set'], args['set'], 1)
cv.imwrite(destination, img[tl_x:tl_x+200, tl_y:tl_y+200])

tl_x, tl_y = 160, 525
destination = destination_path % (args['set'], args['set'], 2)
cv.imwrite(destination, img[tl_x:tl_x+200, tl_y:tl_y+200])

tl_x, tl_y = 260, 525
destination = destination_path % (args['set'], args['set'], 3)
cv.imwrite(destination, img[tl_x:tl_x+200, tl_y:tl_y+200])
