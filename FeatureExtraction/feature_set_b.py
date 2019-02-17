import numpy as np
from scipy.stats import mode
from scipy.stats import skew


FEATURE_VECTOR_SIZE = 42


# extracts the following statistics from each color channel:
#   mean, variance, standard deviation, median, mode, skew, x centroid,
#   y centroid, x standard deviation, y standard deviation, x skew, y skew,
#   x kurtosis, y kurtosis
def get_statistics(image, channels):
    stats = np.zeros(FEATURE_VECTOR_SIZE)

    for i, channel in enumerate(channels):
        current_channel = image[:, :, i]

        h, w = np.shape(current_channel)

        x = np.array(range(w))
        y = np.array(range(h))

        # calculate projections along the x and y axes
        yp = np.sum(current_channel, axis=1)
        xp = np.sum(current_channel, axis=0)

        # centroid
        cx = np.sum(x * xp) / np.sum(xp)
        cy = np.sum(y * yp) / np.sum(yp)

        # standard deviation
        x2 = (x - cx) ** 2
        y2 = (y - cy) ** 2

        sx = np.sqrt(np.sum(x2 * xp) / np.sum(xp))
        sy = np.sqrt(np.sum(y2 * yp) / np.sum(yp))

        # skewness
        x3 = (x - cx) ** 3
        y3 = (y - cy) ** 3

        skx = np.sum(xp * x3) / (np.sum(xp) * sx ** 3)
        sky = np.sum(yp * y3) / (np.sum(yp) * sy ** 3)

        # Kurtosis
        x4 = (x - cx) ** 4
        y4 = (y - cy) ** 4
        kx = np.sum(xp * x4) / (np.sum(xp) * sx ** 4)
        ky = np.sum(yp * y4) / (np.sum(yp) * sy ** 4)

        stats[14 * i] = np.mean(current_channel)
        stats[14 * i + 1] = np.var(current_channel)
        stats[14 * i + 2] = np.std(current_channel)
        stats[14 * i + 3] = np.median(current_channel)
        stats[14 * i + 4] = mode(current_channel, axis=None)[0][0]
        stats[14 * i + 5] = skew(current_channel, axis=None)
        stats[14 * i + 6] = cx
        stats[14 * i + 7] = cy
        stats[14 * i + 8] = sx
        stats[14 * i + 9] = sy
        stats[14 * i + 10] = skx
        stats[14 * i + 11] = sky
        stats[14 * i + 12] = kx
        stats[14 * i + 13] = ky

    return stats
