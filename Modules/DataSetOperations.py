import numpy as np
from Modules.Datasets.tiles import get_raw_data_set
from sklearn.model_selection import StratifiedShuffleSplit


def load_tile_data_set(feature_func):
    # fetch the raw image set and labels
    image_set, y, channels, test_image_set, test_y = get_raw_data_set()

    manual = len(test_image_set) != 0 and len(test_y) != 0

    if not manual:
        # generate feature matrix from image set
        X = np.vstack([feature_func(img, channels) for img, _ in image_set])

        # split training and testing set
        n_splits = 1
        test_set_size = 0.3
        random_state = 6117
        sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size, random_state=random_state)
        train_index, test_index = next(sss.split(X, y))
        X_train, y_train = X[train_index], y[train_index]
        X_test, y_test = X[test_index], y[test_index]

    else:
        X_train = np.vstack([feature_func(img, channels) for img, _ in image_set])
        y_train = y
        X_test = np.vstack([feature_func(img, channels) for img, _ in test_image_set])
        y_test = test_y

    # avoid data copy
    assert X_train.flags['C_CONTIGUOUS']
    assert X_test.flags['C_CONTIGUOUS']
    assert y_train.flags['C_CONTIGUOUS']
    assert y_test.flags['C_CONTIGUOUS']

    return X_train, y_train, X_test, y_test
