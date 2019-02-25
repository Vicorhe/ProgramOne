import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.neighbors import NearestCentroid
from Datasets.tiles import get_raw_data_set
# from FeatureExtraction.feature_set_b import get_statistics
from FeatureExtraction.feature_set_a import get_statistics
from Utilities.utils import unison_shuffled_copies


# fetch the raw training and testing images, and respective labels
training_images, testing_images, y_train, y_test, channels = get_raw_data_set()

# gather features
X_train = np.vstack([get_statistics(img, channels) for img, _ in training_images])
X_test = np.vstack([get_statistics(img, channels) for img, _ in testing_images])
X_train, y_train = unison_shuffled_copies(X_train, y_train)

# avoid data copy
assert X_train.flags['C_CONTIGUOUS']
assert X_test.flags['C_CONTIGUOUS']
assert y_train.flags['C_CONTIGUOUS']
assert y_test.flags['C_CONTIGUOUS']

# nearest centroids classifier
nearest_centroid_clf = Pipeline([
    ('nearest_centroids_clf', NearestCentroid())
])
#   shrink_threshold: 0.2

nearest_centroid_clf.fit(X_train, y_train)

print("training score: %f" % (nearest_centroid_clf.score(X_train, y_train)))
print("testing score: %f" % (nearest_centroid_clf.score(X_test, y_test)))
