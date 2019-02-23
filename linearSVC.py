import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import LinearSVC
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

# linear support vector classifier

random_state = 6117
tol = 1e-06
C = 0.1
penalty = 'l2'
loss = 'hinge'
dual = True
max_iter = 2000

linear_SVC = Pipeline([
    ('linear_svc', LinearSVC(random_state=random_state, tol=tol, C=C,
                             penalty=penalty, loss=loss, dual=dual,
                             max_iter=max_iter))
])

#   C = 10, 5, 1, 0.5, 0.1, 0.001, 0.0001
#   penalty = 'l1', 'l2'
#   loss = 'hinge', 'squared_hinge'
#   dual = True, False
#   max_iter = 500, 1000, 1500, 2000, 2500


linear_SVC.fit(X_train, y_train)

print("training score: %f" % (linear_SVC.score(X_train, y_train)))
print("testing score: %f" % (linear_SVC.score(X_test, y_test)))
