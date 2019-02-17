import numpy as np
from scipy.stats import mode
from scipy.stats import skew, kurtosis


FEATURE_VECTOR_SIZE = 15


def get_statistics(image, channels):
    stats = np.zeros(FEATURE_VECTOR_SIZE)

    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        stats[5 * i] = np.mean(current_channel)
        stats[5 * i + 1] = mode(current_channel, axis=None)[0][0]
        stats[5 * i + 2] = np.var(current_channel)
        stats[5 * i + 3] = kurtosis(current_channel, axis=None)
        stats[5 * i + 4] = skew(current_channel, axis=None)

    return stats
