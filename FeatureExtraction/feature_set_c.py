import numpy as np
import cv2 as cv


FEATURE_VECTOR_SIZE = 7


def get_statistics(image, channels):
    stats = np.zeros(FEATURE_VECTOR_SIZE)

    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        stats[2 * i] = np.mean(current_channel)
        stats[2 * i + 1] = np.var(current_channel)

    cv.cvtColor(image, cv.COLOR_HSV2BGR)
    cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    stats[6] = np.mean(image)
    return stats


def get_feature_names():
    return np.array(['C1 mean', 'C1 mode', 'C1 variance', 'C1 skew', 'C1 kurtosis',
                     'C2 mean', 'C2 mode', 'C2 variance', 'C2 skew', 'C2 kurtosis',
                     'C3 mean', 'C3 mode', 'C3 variance', 'C3 skew', 'C3 kurtosis'])
