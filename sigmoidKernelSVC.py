from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from DATASETOPS import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set()


# sigmoid kernel support vector classifier

kernel = 'sigmoid'
C = 1
gamma = 'scale'
coef0 = 0.0
shrinking = True
tol = 1e-3
max_iter = -1

sigmoid_kernel_SVC = Pipeline([
    ('sigmoid_kernel_svc', SVC(kernel=kernel, C=C, gamma=gamma, coef0=coef0,
                               shrinking=shrinking, tol=tol, max_iter=max_iter))
]).fit(X_train, y_train)
#   C = 0.001, 0.01, 0.1, 1, 10, 100
#   gamma = 'scale', 'auto'
#   coef0 = 0.0, 0.5, 1.0, 2.0
#   shrinking = True, False
#   tol = 1e-2, 1e-3, 1e-4
#   max_iter = -1, 1000, 2000, 3000, 4000


# cross validation
cross_validation_report(sigmoid_kernel_SVC, X_train, y_train)
