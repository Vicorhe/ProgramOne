import numpy as np
import scipy.misc
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from skimage import color
from matplotlib import pyplot as plt


image_filename = '/Users/victorhe/Desktop/lena.png'
n = 20


def quantize(raster, n_colors):
    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    palette = shuffle(reshaped_raster)[:n_colors]

    labels = pairwise_distances_argmin(reshaped_raster, palette)

    quantized_raster = np.reshape(palette[labels], (width, height, palette.shape[1]))

    return quantized_raster


raster = scipy.misc.imread(image_filename)

lab_raster = color.rgb2lab(raster)

q_rgb = quantize(raster, n)
q_lab = quantize(lab_raster, n)

q_lab_as_rgb = (color.lab2rgb(q_lab) * 255).astype('uint8')

plt.imshow(q_lab_as_rgb)
plt.draw()
plt.show()
