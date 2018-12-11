import cv2 as cv
import numpy as np


def image_statistics(image):
    # Input: Z, a 2D array, hopefully containing some sort of peak
    # Output: cx,cy,sx,sy,skx,sky,kx,ky
    # cx and cy are the coordinates of the centroid
    # sx and sy are the standard deviation in the x and y directions
    # skx and sky are the skewness in the x and y directions
    # kx and ky are the Kurtosis in the x and y directions
    # Note: this is not the excess kurtosis. For a normal distribution
    # you expect the kurtosis will be 3.0. Just subtract 3 to get the
    # excess kurtosis.

    h, w = np.shape(image)

    x = range(w)
    y = range(h)

    # calculate projections along the x and y axes
    yp = np.sum(image, axis=1)
    xp = np.sum(image, axis=0)

    # centroid
    cx = np.sum(x*xp)/np.sum(xp)
    cy = np.sum(y*yp)/np.sum(yp)

    # standard deviation
    x2 = (x-cx)**2
    y2 = (y-cy)**2

    sx = np.sqrt(np.sum(x2*xp)/np.sum(xp))
    sy = np.sqrt(np.sum(y2*yp)/np.sum(yp))

    # skewness
    x3 = (x-cx)**3
    y3 = (y-cy)**3

    skx = np.sum(xp*x3)/(np.sum(xp) * sx**3)
    sky = np.sum(yp*y3)/(np.sum(yp) * sy**3)

    # Kurtosis
    x4 = (x-cx)**4
    y4 = (y-cy)**4
    kx = np.sum(xp*x4)/(np.sum(xp) * sx**4)
    ky = np.sum(yp*y4)/(np.sum(yp) * sy**4)

    return cx, cy, sx, sy, skx, sky, kx, ky


def get_color_features_from_image(img):
    return (np.mean(img[:, :, 2]), np.std(img[:, :, 2]),
            np.mean(img[:, :, 1]), np.std(img[:, :, 1]),
            np.mean(img[:, :, 0]), np.std(img[:, :, 0]))


img_1_a = cv.imread('/Users/victorhe/Pictures/colorSamples/1_a.png')
img_1_b = cv.imread('/Users/victorhe/Pictures/colorSamples/1_b.png')
img_2_a = cv.imread('/Users/victorhe/Pictures/colorSamples/2_a.png')
img_2_b = cv.imread('/Users/victorhe/Pictures/colorSamples/2_b.png')
img_3_a = cv.imread('/Users/victorhe/Pictures/colorSamples/3_a.png')
img_3_b = cv.imread('/Users/victorhe/Pictures/colorSamples/3_b.png')

img_4_a = cv.imread('/Users/victorhe/Pictures/colorSamples/4_a.png')
img_4_b = cv.imread('/Users/victorhe/Pictures/colorSamples/4_b.png')
img_5_a = cv.imread('/Users/victorhe/Pictures/colorSamples/5_a.png')
img_5_b = cv.imread('/Users/victorhe/Pictures/colorSamples/5_b.png')
img_6_a = cv.imread('/Users/victorhe/Pictures/colorSamples/6_a.png')
img_6_b = cv.imread('/Users/victorhe/Pictures/colorSamples/6_b.png')

print(get_color_features_from_image(img_1_a))
print(get_color_features_from_image(img_1_b))
print()

print(get_color_features_from_image(img_2_a))
print(get_color_features_from_image(img_2_b))
print()

print(get_color_features_from_image(img_3_a))
print(get_color_features_from_image(img_3_b))
print()

print(get_color_features_from_image(img_4_a))
print(get_color_features_from_image(img_4_b))
print()

print(get_color_features_from_image(img_5_a))
print(get_color_features_from_image(img_5_b))
print()

print(get_color_features_from_image(img_6_a))
print(get_color_features_from_image(img_6_b))


t1 = cv.getTickCount()

# Calculate the image statistics using the projection method
stats_pr = image_statistics(img_1_a[:, :, 0])
print(stats_pr)

t2 = cv.getTickCount()

print('time used: ', (t2 - t1)/cv.getTickFrequency())
