import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit, cross_validate
from sklearn.externals import joblib
from Datasets.tiles import get_data_set
from FeatureExtraction.feature_set_a import get_statistics
from Evaluation.performance import performance_report
from Evaluation.crossValidation import cross_validation_report
# from FeatureExtraction.feature_set_b import get_statistics


# fetch the raw image set and labels
image_set, y, channels = get_data_set()

# generate feature matrix from image set
X = np.vstack([get_statistics(img, channels) for img, _ in image_set])

# split training and testing set
n_splits = 1
test_set_size = 0.3
random_state = 6117
sss = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_set_size, random_state=random_state)
train_index, test_index = next(sss.split(X, y))
X_train, y_train = X[train_index], y[train_index]
X_test, y_test = X[test_index], y[test_index]

# avoid data copy
assert X_train.flags['C_CONTIGUOUS']
assert X_test.flags['C_CONTIGUOUS']
assert y_train.flags['C_CONTIGUOUS']
assert y_test.flags['C_CONTIGUOUS']

# k nearest neighbors classifier

n_neighbors = 3
k_nearest_neighbors_clf = Pipeline([
    ('k_nearest_neighbors_clf', KNeighborsClassifier(n_neighbors=n_neighbors,
                                                     weights='uniform'))
])
#   n_neighbors: 3, 5, 7, 9, 11
#   weights: 'uniform', 'distance'

k_nearest_neighbors_clf.fit(X_train, y_train)

# cross validation
cross_validation_report(k_nearest_neighbors_clf, X_train, y_train)

# train_predict = k_nearest_neighbors_clf.predict(X_train)
# test_predict = k_nearest_neighbors_clf.predict(X_test)

# performance_report(y_train, train_predict, y_test, test_predict)
