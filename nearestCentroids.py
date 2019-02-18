import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.neighbors import NearestCentroid
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

# nearest centroids classifier
nc_clf = Pipeline([
    ('k_centroids', NearestCentroid())
])
#   shrink_threshold: 0.2

nc_clf.fit(X_train, y_train)

print("training score: %f" % (nc_clf.score(X_train, y_train)))
print("testing score: %f" % (nc_clf.score(X_test, y_test)))
