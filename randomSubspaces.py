import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
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

# random subspaces classifier

base_estimator = DecisionTreeClassifier()
n_estimators = 10
max_samples = 1.0
max_features = 0.5
bootstrap = False
bootstrap_features = True
n_jobs = -1

random_subspaces_clf = Pipeline([
    ('random_subspaces_clf', BaggingClassifier(base_estimator=base_estimator,
                                               n_estimators=n_estimators,
                                               max_samples=max_samples,
                                               max_features=max_features,
                                               bootstrap=bootstrap,
                                               bootstrap_features=bootstrap_features,
                                               n_jobs=n_jobs))
])
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_features = 0.25, 0.5, 0.67, 0.8

random_subspaces_clf.fit(X_train, y_train)

print("training score: %f" % (random_subspaces_clf.score(X_train, y_train)))
print("testing score: %f" % (random_subspaces_clf.score(X_test, y_test)))