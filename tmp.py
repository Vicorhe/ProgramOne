import cv2 as cv
import numpy as np

p = '/Users/victorhe/Pictures/batch_8/image_95.BMP'

i = cv.imread(p)
cv.rectangle(i, (0, 152), (1600, 655), (0, 255, 0), 3)
cv.rectangle(i, (0, 725), (1600, 1200), (0, 255, 0), 3)

cv.namedWindow('win1', cv.WINDOW_NORMAL)
cv.namedWindow('win2', cv.WINDOW_NORMAL)
cv.namedWindow('win3', cv.WINDOW_NORMAL)


i_1 = i[152:655, :]
i_2 = i[725:, :]
i_3 = np.concatenate((i_1, i_2), axis=0)
cv.imshow('win1', i_1)
cv.imshow('win2', i_2)
cv.imshow('win3', i_3)

cv.waitKey(0)
cv.destroyAllWindows()
