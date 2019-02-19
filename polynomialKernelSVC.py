import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.svm import SVC
from Miscellaneous.imageAcquisition import get_data_set
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

# polynomial kernel support vector classifier

kernel = 'poly'
C = 1
degree = 3
gamma = 'scale'
coef0 = 0.0
shrinking = True
tol = 1e-3
max_iter = -1

polynomial_kernel_SVC = Pipeline([
    ('polynomial_kernel_svc', SVC(kernel=kernel, C=C, degree=degree,
                                  gamma=gamma, coef0=coef0,
                                  shrinking=shrinking, tol=tol,
                                  max_iter=max_iter))
])

#   C = 0.001, 0.01, 0.1, 1, 10, 100
#   degree = 2, 3, 4, 5
#   gamma = 'scale', 'auto'
#   coef0 = 0.0, 0.5, 1.0, 2.0
#   shrinking = True, False
#   tol = 1e-2, 1e-3, 1e-4
#   max_iter = -1, 1000, 2000, 3000, 4000


polynomial_kernel_SVC.fit(X_train, y_train)

print("training score: %f" % (polynomial_kernel_SVC.score(X_train, y_train)))
print("testing score: %f" % (polynomial_kernel_SVC.score(X_test, y_test)))
