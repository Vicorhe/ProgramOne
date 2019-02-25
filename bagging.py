import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from Datasets.tiles import get_raw_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# fetch the raw image set and labels
image_set, y, channels = get_raw_data_set()

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


# bagging classifier

base_estimator = DecisionTreeClassifier()
n_estimators = 10
max_samples = 0.25
bootstrap = True
oob_score = True
n_jobs = -1

bagging_clf = Pipeline([
    ('bagging_clf', BaggingClassifier(base_estimator=base_estimator,
                                      n_estimators=n_estimators,
                                      max_samples=max_samples,
                                      bootstrap=True,
                                      oob_score=oob_score,
                                      n_jobs=n_jobs))
])
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_samples = 0.25, 0.5, 0.67, 0.8

bagging_clf.fit(X_train, y_train)

print("training score: %f" % (bagging_clf.score(X_train, y_train)))
print("testing score: %f" % (bagging_clf.score(X_test, y_test)))
