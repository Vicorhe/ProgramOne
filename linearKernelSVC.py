from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from Modules.DataSetOperations import load_tile_data_set
from Modules.FeatureExtraction.feature_set_a import get_statistics
# from FeatureExtraction.feature_set_b import get_statistics
from Modules.Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# linear kernel support vector classifier

kernel = 'linear'
C = 1
shrinking = True
tol = 1e-3
max_iter = -1

linear_kernel_SVC = Pipeline([
    ('linear_kernel_svc', SVC(kernel=kernel, C=C, shrinking=shrinking,
                              tol=tol, max_iter=max_iter))
]).fit(X_train, y_train)
#   C = 0.001, 0.01, 0.1, 1, 10, 100
#   shrinking = True, False
#   tol = 1e-2, 1e-3, 1e-4
#   max_iter = -1, 1000, 2000, 3000, 4000


# cross validation
cross_validation_report(linear_kernel_SVC, X_train, y_train)
