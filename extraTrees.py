import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.ensemble import ExtraTreesClassifier
from Datasets.tiles import get_data_set
from FeatureExtraction.feature_set_b import get_statistics
# from FeatureExtraction.feature_set_a import get_statistics
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

# extra trees classifier

n_estimators = 10
criterion = 'gini'
max_depth = 4
max_features = 'sqrt'
bootstrap = True
n_jobs = -1

extra_trees_clf = Pipeline([
    ('extra_trees_clf', ExtraTreesClassifier(n_estimators=n_estimators,
                                                 criterion=criterion,
                                                 max_depth=max_depth,
                                                 max_features=max_features,
                                                 bootstrap=True,
                                                 n_jobs=n_jobs))
])
#   n_estimators = 10, 50, 100, 300, 500
#   criterion = 'gini', 'entropy'
#   max_depth = 2, 4, 6, 8, 10
#   max_features = 'sqrt', 'log2', None

extra_trees_clf.fit(X_train, y_train)

print("training score: %f" % (extra_trees_clf.score(X_train, y_train)))
print("testing score: %f" % (extra_trees_clf.score(X_test, y_test)))
