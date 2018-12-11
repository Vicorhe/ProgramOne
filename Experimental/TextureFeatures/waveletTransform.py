import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

import pywt
import pywt.data


# Load image
original = cv.imread('/Users/victorhe/Desktop/textureSamples/texture3b.png', 0)
original = cv.imread('/Users/victorhe/Desktop/homeSourceTiles/live_y_2.jpeg', 0)

print(type(original))


# Wavelet transform of image, and plot approximation and details
titles = ['Approximation', ' Horizontal detail',
          'Vertical detail', 'Diagonal detail']
coeffs2 = pywt.dwt2(original, 'bior1.3')
LL, (LH, HL, HH) = coeffs2
fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()