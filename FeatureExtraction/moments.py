import numpy as np


FEATURE_VECTOR_SIZE = 24


# Input: Z, a 2D array, hopefully containing some sort of peak
# Output: cx,cy,sx,sy,skx,sky,kx,ky
# cx and cy are the coordinates of the centroid
# sx and sy are the standard deviation in the x and y directions
# skx and sky are the skewness in the x and y directions
# kx and ky are the Kurtosis in the x and y directions
# Note: this is not the excess kurtosis. For a normal distribution
# you expect the kurtosis will be 3.0. Just subtract 3 to get the
# excess kurtosis.
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

        stats[8 * i] = cx
        stats[8 * i + 1] = cy
        stats[8 * i + 2] = sx
        stats[8 * i + 3] = sy
        stats[8 * i + 4] = skx
        stats[8 * i + 5] = sky
        stats[8 * i + 6] = kx
        stats[8 * i + 7] = ky

    return stats

