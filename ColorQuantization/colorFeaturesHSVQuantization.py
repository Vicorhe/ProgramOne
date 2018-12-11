import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def get_color_features_from_image(img):
    hsv_hist = get_hsv_hist(img)
    top_k_colors = get_top_k_colors_from_hist(hsv_hist, 3)
    color_features = get_color_features_from_top_k_colors(top_k_colors)
    return color_features


# TODO optimize a ton, consider convolution
def get_hsv_hist(bgr_img):
    hsv_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2HSV)
    h, w = hsv_img.shape[:2]
    quantized_img = np.zeros((h, w), np.uint8)

    # t1 = cv.getTickCount()

    for row in range(h):
        for col in range(w):
            quantized_img[row, col] = pixel_quantization(hsv_img[row, col])

    hist = cv.calcHist([quantized_img], [0], None, [72], [0, 71])

    # t2 = cv.getTickCount()
    # print('time used in seconds: %s' % ((t2 - t1) / cv.getTickFrequency()))

    return hist


def pixel_quantization(pixel):
    h, s, v = pixel
    return 9 * get_h(h) + 3 * get_s(s) + get_v(v)


def get_h(h_val):
    if h_val >= 158 or h_val <= 10:
        return 0
    elif h_val <= 20:
        return 1
    elif h_val <= 37:
        return 2
    elif h_val <= 77:
        return 3
    elif h_val <= 95:
        return 4
    elif h_val <= 135:
        return 5
    elif h_val <= 147:
        return 6
    else:
        return 7


def get_v(v_val):
    percentage = v_val / 255
    if percentage < 0.2:
        return 0
    elif percentage < 0.7:
        return 1
    else:
        return 2


def get_s(s_val):
    percentage = s_val / 255
    if percentage < 0.2:
        return 0
    elif percentage < 0.7:
        return 1
    else:
        return 2


def get_top_k_colors_from_hist(hist, k):
    hist = enumerate(hist.ravel())
    sorted_hist = sorted(hist, key=lambda x: x[1], reverse=True)
    top_k_colors = [c for c, v in sorted_hist[:k]]
    return top_k_colors


def get_color_features_from_top_k_colors(top_colors):
    return np.average(top_colors), np.std(top_colors)


'''
img_1_a = cv.imread('/Users/victorhe/Pictures/colorSamples/1_a.png')
img_1_b = cv.imread('/Users/victorhe/Pictures/colorSamples/1_b.png')
img_2_a = cv.imread('/Users/victorhe/Pictures/colorSamples/2_a.png')
img_2_b = cv.imread('/Users/victorhe/Pictures/colorSamples/2_b.png')
img_3_a = cv.imread('/Users/victorhe/Pictures/colorSamples/3_a.png')
img_3_b = cv.imread('/Users/victorhe/Pictures/colorSamples/3_b.png')
'''

img_4_a = cv.imread('/Users/victorhe/Pictures/colorSamples/4_a.png')
img_4_b = cv.imread('/Users/victorhe/Pictures/colorSamples/4_b.png')
img_5_a = cv.imread('/Users/victorhe/Pictures/colorSamples/5_a.png')
img_5_b = cv.imread('/Users/victorhe/Pictures/colorSamples/5_b.png')
img_6_a = cv.imread('/Users/victorhe/Pictures/colorSamples/6_a.png')
img_6_b = cv.imread('/Users/victorhe/Pictures/colorSamples/6_b.png')


hist_4_a = get_hsv_hist(img_4_a)
hist_4_b = get_hsv_hist(img_4_b)
hist_5_a = get_hsv_hist(img_5_a)
hist_5_b = get_hsv_hist(img_5_b)
hist_6_a = get_hsv_hist(img_6_a)
hist_6_b = get_hsv_hist(img_6_b)



plt.subplot(2, 6, 1), plt.imshow(img_4_a), plt.title('4_a_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 2), plt.plot(hist_4_a), plt.title('4_a'), plt.xticks([]), plt.yticks([])

plt.subplot(2, 6, 3), plt.imshow(img_5_a), plt.title('5_a_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 4), plt.plot(hist_5_a), plt.title('5_a'), plt.xticks([]), plt.yticks([])

plt.subplot(2, 6, 5), plt.imshow(img_6_a), plt.title('6_a_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 6), plt.plot(hist_6_a), plt.title('6_a'), plt.xticks([]), plt.yticks([])

plt.subplot(2, 6, 7), plt.imshow(img_4_b), plt.title('4_b_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 8), plt.plot(hist_4_b), plt.title('4_b'), plt.xticks([]), plt.yticks([])

plt.subplot(2, 6, 9), plt.imshow(img_5_b, cmap='brg'), plt.title('5_b_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 10), plt.plot(hist_5_b), plt.title('5_b'), plt.xticks([]), plt.yticks([])

plt.subplot(2, 6, 11), plt.imshow(img_6_b), plt.title('6_b_img'), plt.xticks([]), plt.yticks([])
plt.subplot(2, 6, 12), plt.plot(hist_6_b), plt.title('6_b'), plt.xticks([]), plt.yticks([])

plt.show()


# t3 = cv.getTickCount()
'''
print('4a: ', get_color_features_from_image(img_4_a))
print('4b: ', get_color_features_from_image(img_4_b))
print('5a: ', get_color_features_from_image(img_5_a))
print('5b: ', get_color_features_from_image(img_5_b))
print('6a: ', get_color_features_from_image(img_6_a))
print('6b: ', get_color_features_from_image(img_6_b))
'''
# t4 = cv.getTickCount()
# print('time taken to xxx: %s s' % ((t4-t3)/cv.getTickFrequency()))
