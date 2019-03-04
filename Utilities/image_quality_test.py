from random import randint
import cv2 as cv

name = 'a'
SOURCE_PATH = '/Users/victorhe/Pictures/' + name + '.BMP'
DESTINATION_PATH = '/Users/victorhe/Pictures/test/' + name + '_%d.BMP'
SAMPLE_COUNT = 10


def crop_center(image):
    h, w = image.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2
    return image[mid_h - 500: mid_h + 500, mid_w - 500: mid_w + 500]


img = cv.imread(SOURCE_PATH)
cropped_img = crop_center(img)

for i in range(SAMPLE_COUNT):
    tl_x, tl_y = randint(0, 19) * 25, randint(0, 19) * 25
    print(tl_x, tl_y)
    destination = DESTINATION_PATH % i
    cv.imwrite(destination, cropped_img[tl_x:tl_x+500, tl_y:tl_y+500])

