import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def get_texture_input_dataset():
    img_1a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture1a.png', 0)
    img_1b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture1b.png', 0)

    img_2a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture2a.png', 0)
    img_2b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture2b.png', 0)

    img_3a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture3a.png', 0)
    img_3b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture3b.png', 0)

    img_4a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture4a.png', 0)
    img_4b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture4b.png', 0)

    img_5a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture5a.png', 0)
    img_5b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture5b.png', 0)

    img_6a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture6a.png', 0)
    img_6b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture6b.png', 0)

    img_7a = cv.imread('/Users/victorhe/Desktop/textureSamples/texture7a.png', 0)
    img_7b = cv.imread('/Users/victorhe/Desktop/textureSamples/texture7b.png', 0)

    return img_1a, img_1b, img_2a, img_2b, img_3a, img_3b, img_4a, img_4b, img_5a, img_5b, img_6a, img_6b, img_7a, img_7b


def sobel_demo(img):
    sobel_x = cv.Sobel(img, -1, 0, 1)
    sobel_y = cv.Sobel(img, -1, 1, 0)
    sobel = cv.addWeighted(sobel_y, 0.5, sobel_x, 0.5, 0)
    cv.imshow('sobel', sobel * 5)
    return sobel


def canny_demo(img):
    canny = cv.Canny(img, 20, 70)
    cv.imshow('canny', canny)
    return canny


def morphology_rect_demo(img):
    kernel_rect = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    dif_rect = cv.dilate(img, kernel_rect) - cv.erode(img, kernel_rect)
    cv.imshow('dif-rect', dif_rect * 5)
    return dif_rect


def morphology_ellipse_demo(img):
    kernel_ellipse = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    dif_ellipse = cv.dilate(img, kernel_ellipse) - cv.erode(img, kernel_ellipse)
    cv.imshow('dif-ellipse', dif_ellipse * 5)
    return dif_ellipse


def morphology_cross_demo(img):
    kernel_cross = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    dif_cross = cv.dilate(img, kernel_cross) - cv.erode(img, kernel_cross)
    cv.imshow('dif-cross', dif_cross * 5)
    return dif_cross


def get_hu_features(edges):
    return cv.HuMoments(cv.moments(edges))


def test_script(img1, img2):
    plt.subplot(121), plt.imshow(img1), plt.title('Image 1'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img2), plt.title('Image 1'), plt.xticks([]), plt.yticks([])
    plt.show()

    edges_1 = morphology_cross_demo(img1)
    edges_2 = morphology_cross_demo(img2)

    # ellipse = morphology_ellipse_demo(img)
    # rect = morphology_rect_demo(img)

    hu_1 = get_hu_features(edges_1)
    hu_2 = get_hu_features(edges_2)

    print(np.hstack((hu_1, hu_2)))


img_1a, img_1b, img_2a, img_2b, img_3a, img_3b, img_4a, img_4b, img_5a, img_5b, img_6a, img_6b, img_7a, img_7b \
    = get_texture_input_dataset()

# huM_1 = cv.HuMoments(cv.moments(dif_rect_1))
# huM_2 = cv.HuMoments(cv.moments(dif_rect_2))

# print(huM_1)
# print(huM_2)

# original_1 = cv.imread('/Users/victorhe/Desktop/sourceTiles/multi2.png', 0)
# original_2 = cv.imread('/Users/victorhe/Desktop/sourceTiles/multi3.png', 0)


test_script(img_4b, img_4a)


cv.waitKey(0)
cv.destroyAllWindows()
