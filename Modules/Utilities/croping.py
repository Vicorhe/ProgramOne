from glob import glob
import cv2 as cv


def crop_center(image):
    h, w = image.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2
    return image[mid_h - 500: mid_h + 500, mid_w - 500: mid_w + 500]


for path in sorted(glob('/Users/victorhe/Pictures/studioSourceTiles/SS7/*.BMP')):
    img = cv.imread(path)
    filename = path.split('/')[-1]
    filename_with_path = '/Users/victorhe/Pictures/studioSourceTiles/SS7/cropped/%s' % filename

    result_img = crop_center(img)

    print(filename_with_path)
    cv.imwrite(filename_with_path, result_img)

