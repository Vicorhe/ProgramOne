import numpy as np


def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]


def crop_center(image):
    h, w = image.shape[:-1]
    mid_h = h // 2
    mid_w = w // 2
    return image[mid_h - 500: mid_h + 500, mid_w - 500: mid_w + 500]
