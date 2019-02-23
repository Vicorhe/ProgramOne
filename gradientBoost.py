import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.ensemble import GradientBoostingClassifier
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

# gradient boost classifier

loss = 'deviance'
learning_rate = 0.1
n_estimators = 100
subsample = 1.0
criterion = 'friedman_mse'
max_depth = 3
max_features = 'sqrt'

gradient_boost_clf = Pipeline([
    ('ada_boost_clf', GradientBoostingClassifier(loss=loss,
                                                 learning_rate=learning_rate,
                                                 n_estimators=n_estimators,
                                                 subsample=subsample,
                                                 criterion=criterion,
                                                 max_depth=max_depth,
                                                 max_features=max_features))
])
#   loss = 'deviance', 'exponential'
#   learning_rate = 0.1, 0.2, 0.3, 0.5, 0.7, 1.0
#   n_estimators = 25, 50, 100, 200
#   subsample = 0.1, 0.25, 0.5, 0.75, 1.0
#   criterion = 'friedman_mse', 'mse', 'mae'
#   max_depth = 2, 4, 6, 8, 10
#   max_features = 'sqrt', 'log2', None

gradient_boost_clf.fit(X_train, y_train)

print("training score: %f" % (gradient_boost_clf.score(X_train, y_train)))
print("testing score: %f" % (gradient_boost_clf.score(X_test, y_test)))
