import argparse
from glob import glob
import cv2 as cv


source_path = '/Users/victorhe/Pictures/studioSourceTiles/%s/*'
destination_path = '/Users/victorhe/Pictures/studioSourceTiles/GROUP_%d/%s_%d.BMP'


ap = argparse.ArgumentParser()
ap.add_argument('-s', '--set', required=True, help='set of images being evaluated')
ap.add_argument('-g', '--group', required=True, help='set of images being evaluated', type=int)
args = vars(ap.parse_args())
image_set = list()

for path in sorted(glob(source_path % args['set'])):
    img = cv.imread(path)
    image_set.append(img)

# works on BMP images
counter = 1
for img in image_set:
    h, w = img.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2

    image_splits = [img[:mid_h, :mid_w], img[:mid_h, mid_w:w], img[mid_h:h, :mid_w], img[mid_h:h, mid_w:w]]

    for i in range(4):
        filename = destination_path % (args['group'], args['set'], counter)
        cv.imwrite(filename, image_splits[i])
        print(filename)
        counter += 1
