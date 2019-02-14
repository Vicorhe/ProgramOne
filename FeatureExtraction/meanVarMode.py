import numpy as np
from scipy.stats import mode


FEATURE_VECTOR_SIZE = 9


def get_statistics(image, channels):
    stats = np.zeros(FEATURE_VECTOR_SIZE)

    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        # print('%s mean: %f' % (channel, np.mean(current_channel)), end=' ')
        # print('%s vari: %f' % (channel, np.var(current_channel)), end=' ')
        # print('%s mode: %f' % (channel, mode(current_channel, axis=None)[0][0]), end=' ')

        stats[3*i] = np.mean(current_channel)
        stats[3*i+1] = np.var(current_channel)
        stats[3*i+2] = mode(current_channel, axis=None)[0][0]

    # print()
    return stats
