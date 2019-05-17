"""
ONLY RUN THIS CODE ON WINDOWS MACHINE
Used to trying out the ROI for used for feature extraction
"""
import cv2 as cv
from sys import platform

if platform == "darwin":
    raise OSError('This script should only be ran on Windows OS.')

# change the following as circumstances require
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures\\TrainingBatches\\test_dif\\batch_0\\image_%d.BMP'


for i in range(16):
    img = cv.imread(WINDOWS_PICTURES_PATH % i)
    cv.namedWindow('win', cv.WINDOW_KEEPRATIO)
    cv.imshow('win', img[150:1050, 300:1200])

    cv.waitKey(0)

cv.destroyAllWindows()
