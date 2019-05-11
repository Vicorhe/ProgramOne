import numpy as np


FEATURE_VECTOR_SIZE = 6


def get_statistics(image):
    stats = np.zeros(FEATURE_VECTOR_SIZE)
    for i in range(3):
        current_channel = image[:, :, i]
        stats[2*i] = np.mean(current_channel)
        stats[2*i+1] = np.var(current_channel)
    return stats


def get_feature_names():
    return ['H mean', 'H variance', 'S mean', 'S variance', 'V mean', 'V variance']
