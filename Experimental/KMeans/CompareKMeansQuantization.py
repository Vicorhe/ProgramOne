import numpy as np
import scipy.misc
from sklearn import cluster
from sklearn.metrics import pairwise_distances_argmin
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
    model_m = cluster.MiniBatchKMeans(n_clusters=n_colors)
    model_m.fit(reshaped_raster)
    print("mini batch kmeans training done in %0.3fs." % (time() - t_2))

    t_3 = time()
    labels = model.predict(reshaped_raster)
    print("kmeans predict mapping done in %0.3fs." % (time() - t_3))

    t_4 = time()
    labels_m = model_m.predict(reshaped_raster)
    print("mini batch kmeans predict mapping done in %0.3fs." % (time() - t_4))

    palette = model.cluster_centers_
    palette_m = model_m.cluster_centers_

    t_5 = time()
    labels_ = pairwise_distances_argmin(reshaped_raster, palette)
    print("pairwise kmeans mapping done in %0.3fs." % (time() - t_5))

    t_6 = time()
    labels_m_ = pairwise_distances_argmin(reshaped_raster, palette_m)
    print("pairwise mini batch kmeans mapping done in %0.3fs." % (time() - t_6))

    print(all(labels_ == labels))
    print(all(labels_m == labels_m_))

    t_7 = time()
    quantized_raster = np.reshape(palette[labels], (width, height, palette.shape[1]))
    quantized_raster = np.reshape(palette_m[labels_m], (width, height, palette_m.shape[1]))
    print("done in %0.3fs." % (time() - t_7))

    return quantized_raster


raster = scipy.misc.imread(image_filename)

hsv_raster = color.rgb2hsv(raster)

# q_rgb = quantize(raster, n)
q_hsv = quantize(hsv_raster, n)

q_hsv_as_rgb = color.hsv2rgb(q_hsv)# * 255).astype('uint8')

plt.imshow(q_hsv_as_rgb)
plt.draw()
plt.show()
