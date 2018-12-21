import numpy as np
import scipy.misc
from sklearn import cluster
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from skimage import color
from matplotlib import pyplot as plt

from time import time


image_filename = '/Users/victorhe/Desktop/lena.png'
n = 20


def quantize(raster, n_colors):

    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    t_1 = time()
    model = cluster.KMeans(n_clusters=n_colors)
    model.fit(reshaped_raster)
    print("kmeans training done in %0.3fs." % (time() - t_1))

    t_2 = time()
    labels = model.predict(reshaped_raster)
    print("predict mapping done in %0.3fs." % (time() - t_2))

    palette = model.cluster_centers_

    t_3 = time()
    labels_ = pairwise_distances_argmin(reshaped_raster, palette)
    print("pairwise mapping done in %0.3fs." % (time() - t_3))

    print(all(labels_ == labels))

    quantized_raster = np.reshape(palette[labels], (width, height, palette.shape[1]))

    print("done in %0.3fs." % (time() - t_1))
    return quantized_raster


raster = scipy.misc.imread(image_filename)

lab_raster = color.rgb2lab(raster)

# q_rgb = quantize(raster, n)
q_lab = quantize(lab_raster, n)

q_lab_as_rgb = (color.lab2rgb(q_lab) * 255).astype('uint8')

plt.imshow(q_lab_as_rgb)
plt.draw()
plt.show()
