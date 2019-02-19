import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.neighbors import KNeighborsClassifier
from Miscellaneous.imageAcquisition import get_data_set
# from FeatureExtraction.feature_set_b import get_statistics
from FeatureExtraction.feature_set_a import get_statistics
from Utilities.utils import unison_shuffled_copies


# fetch the raw training and testing images, and respective labels
training_images, testing_images, y_train, y_test, channels = get_data_set()

# gather features
X_train = np.vstack([get_statistics(img, channels) for img, _ in training_images])
X_test = np.vstack([get_statistics(img, channels) for img, _ in testing_images])
X_train, y_train = unison_shuffled_copies(X_train, y_train)

# avoid data copy
assert X_train.flags['C_CONTIGUOUS']
assert X_test.flags['C_CONTIGUOUS']
assert y_train.flags['C_CONTIGUOUS']
assert y_test.flags['C_CONTIGUOUS']

# k nearest neighbors classifier

n_neighbors = 3

knn_clf = Pipeline([
    ('k_neighbors', KNeighborsClassifier(n_neighbors=n_neighbors, weights='uniform'))
])
#   n_neighbors: 3, 5, 7, 9, 11
#   weights: 'uniform', 'distance'

knn_clf.fit(X_train, y_train)

print("training score: %f" % (knn_clf.score(X_train, y_train)))
print("testing score: %f" % (knn_clf.score(X_test, y_test)))
