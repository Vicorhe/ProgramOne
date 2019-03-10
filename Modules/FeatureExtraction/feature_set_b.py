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
        stats[5 * i + 3] = skew(current_channel, axis=None)
        stats[5 * i + 4] = kurtosis(current_channel, axis=None)

    return stats


def get_feature_names():
    return np.array(['C1 mean', 'C1 mode', 'C1 variance', 'C1 skew', 'C1 kurtosis',
                     'C2 mean', 'C2 mode', 'C2 variance', 'C2 skew', 'C2 kurtosis',
                     'C3 mean', 'C3 mode', 'C3 variance', 'C3 skew', 'C3 kurtosis'])
