import numpy as np


FEATURE_VECTOR_SIZE = 6


def get_statistics(image, channels):
    stats = np.zeros(FEATURE_VECTOR_SIZE)

    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        # print('%s mean: %f' % (channel, np.mean(current_channel)), end=' ')
        # print('%s vari: %f' % (channel, np.var(current_channel)), end=' ')

        stats[2*i] = np.mean(current_channel)
        stats[2*i+1] = np.var(current_channel)

    # print()
    return stats


