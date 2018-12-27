import argparse
from glob import glob
import numpy as np
import scipy.misc
from sklearn.cluster import MiniBatchKMeans, KMeans
from skimage import color
from matplotlib import pyplot as plt
from sklearn.externals import joblib
from time import time
import os.path
import cv2 as cv


ap = argparse.ArgumentParser()
ap.add_argument('-set', required=True, help='set of images being evaluated')
ap.add_argument('-num', required=True, type=int, help="size of color palette")
ap.add_argument('--mini-batch', dest='use_mini_batch', action='store_true', help='use mini batch kmeans')
ap.add_argument('--train', dest='train_new_model', action='store_true', help='train a new a model')
args = vars(ap.parse_args())


model_pkg_name = 'models/%s_%s_%s_model.pkl' % \
                 (args['set'], args['num'], 'mini_batch' if args['use_mini_batch'] else 'kmeans')


def model_does_not_exists(model_path):
    return not os.path.exists(model_path) and not os.path.isfile(model_path)


def get_lab_raster(image_path):
    raster = scipy.misc.imread(image_path)
    lab_raster = color.rgb2lab(raster)
    w, h, d = lab_raster.shape
    reshaped_raster = np.reshape(lab_raster, (w * h, d))
    return reshaped_raster, w, h, d


def train_model():
    training_image_path = '/Users/victorhe/Pictures/colorQuantization/%s/%s_training_image.jpeg' % (
        args['set'], args['set'])

    reshaped_raster, _, _, _ = get_lab_raster(training_image_path)

    model = MiniBatchKMeans(n_clusters=args['num']) \
        if args['use_mini_batch'] else KMeans(n_clusters=args['num'])

    model.fit(reshaped_raster)

    return model


def get_file_name_from_path(file_path):
    return file_path.split('/')[-1]


def get_evaluation_set():
    image_set = glob('/Users/victorhe/Pictures/colorQuantization/%s/*.jpeg' % args['set'])
    return sorted(list(filter(lambda x: x.find('training_image') == -1, image_set)))


def evaluate_set(model, image_set):
    set_size = len(image_set)
    for i, img_path in enumerate(image_set):
        img_name = get_file_name_from_path(img_path)

        reshaped_raster, w, h, d = get_lab_raster(img_path)

        labels = model.predict(reshaped_raster)

        palette = model.cluster_centers_

        quantized_raster = np.reshape(palette[labels], (w, h, palette.shape[1]))
        quantized_rgb = (color.lab2rgb(quantized_raster) * 255).astype('uint8')

        #   cv.imshow('quantized_' + img, cv.cvtColor(quantized_rgb, cv.COLOR_RGB2BGR))

        reshaped_labels = np.reshape(labels, (w, h)).astype('uint8')

        #'''
        plt.subplot(set_size, 2, 2 * i + 1), plt.imshow(quantized_rgb)
        plt.title('quantized_' + img_name), plt.xticks([]), plt.yticks([])

        plt.subplot(set_size, 2, 2 * i + 2), plot_histogram(reshaped_labels)
        plt.title('hist_' + img_name), plt.xticks([]), plt.yticks([])
        #'''

        #   hist = cv.calcHist([reshaped_labels], [0], None, [args['num']], [0, args['num']])
        #   plt.plot(hist, label=img)

    #   plt.xlim([0, args['num']])
    #   plt.legend(bbox_to_anchor=(0., 1.02, 1., .202), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


def plot_histogram(img):
    hist = cv.calcHist([img], [0], None, [args['num']], [0, args['num']])
    plt.plot(hist)
    plt.xlim([0, args['num']])


# get model
if args['train_new_model'] or model_does_not_exists(model_pkg_name):
    print('training new model')
    model = train_model()
else:
    print('using loaded model')
    model = joblib.load(model_pkg_name)

# evaluate image set
image_set = get_evaluation_set()
evaluate_set(model, image_set)

#  saves models
joblib.dump(model, model_pkg_name)

#  cv.waitKey(0)
#  cv.destroyAllWindows()