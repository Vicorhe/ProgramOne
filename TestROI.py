"""
ONLY RUN THIS CODE ON WINDOWS MACHINE
Used to trying out the ROI for used for feature extraction
"""
import cv2 as cv
from sys import platform

if platform == "darwin":
    raise OSError('This script should only be ran on Windows OS.')

# change the following as circumstances require
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures\\TrainingBatches\\three\\batch_1\\image_0.BMP'


img = cv.imread(WINDOWS_PICTURES_PATH)
cv.imshow('win', img[50:1000, 250:1200])

cv.waitKey(0)
cv.destroyAllWindows()
