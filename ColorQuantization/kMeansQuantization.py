import argparse
from glob import glob
import numpy as np
import scipy.misc
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics import pairwise_distances_argmin
from skimage import color
from matplotlib import pyplot as plt
from sklearn.externals import joblib
from time import time
import os.path

ap = argparse.ArgumentParser()
ap.add_argument('-set', required=True, help='set of images being evaluated')
ap.add_argument('-num', required=True, help="size of color palette")
ap.add_argument('--mini-batch', dest='use_mini_batch', action='store_true', help='use mini batch kmeans')
ap.add_argument('--train', dest='train_new_model', action='store_true', help='train a new a model')
args = vars(ap.parse_args())

model_pkg_name = 'models/%s_%s_%s_model.pkl' % \
                 (args['set'], args['num'], 'mini_batch' if args['use_mini_batch'] else 'kmeans')


def model_does_not_exists(model_path):
    return not os.path.exists(model_path) and not os.path.isfile(model_path)


def train_model():
    training_image_name = '/Users/victorhe/Pictures/colorQuantization/%s/%s_training_image.jpeg' % (
        args['set'], args['set'])
    print(training_image_name)

    raster = scipy.misc.imread(training_image_name)

    lab_raster = color.rgb2lab(raster)

    if args['use_mini_batch']:
        model = MiniBatchKMeans(n_clusters=args['num'])
    else:
        model = KMeans(n_clusters=args['num'])

    return model


# get model
if args['train_new_model'] or model_does_not_exists(model_pkg_name):
    model = train_model()
else:
    model = joblib.load(model_pkg_name)

#evaluate model on image set
#dump model


def quantize(raster, n_colors):

    width, height, depth = raster.shape
    reshaped_raster = np.reshape(raster, (width * height, depth))

    t_1 = time()
    model = KMeans(n_clusters=n_colors)
    model.fit(reshaped_raster)
    print("kmeans training done in %0.3fs." % (time() - t_1))

    t_2 = time()
    model_m = MiniBatchKMeans(n_clusters=n_colors)
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


#raster = scipy.misc.imread(image_filename)

#lab_raster = color.rgb2lab(raster)

#q_lab = quantize(lab_raster, n)

#q_lab_as_rgb = (color.lab2rgb(q_lab) * 255).astype('uint8')

#plt.imshow(q_lab_as_rgb)
#plt.draw()
#plt.show()
