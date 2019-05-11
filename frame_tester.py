import cv2 as cv
WINDOWS_PICTURES_PATH = 'C:\\Users\\van32\\Pictures\\TrainingBatches\\three\\batch_1\\image_0.BMP'

img = cv.imread(WINDOWS_PICTURES_PATH)

cv.imshow('win', img[50:1000, 250:1200])

cv.waitKey(0)
cv.destroyAllWindows()