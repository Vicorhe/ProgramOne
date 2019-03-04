from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from Datasets.utils import load_tile_data_set
from FeatureExtraction.feature_set_a import get_statistics
# from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# linear support vector classifier

random_state = 6117
tol = 1e-06
C = 0.1
penalty = 'l2'
loss = 'hinge'
dual = True
max_iter = 5000

linear_SVC = Pipeline([
    ('linear_svc', LinearSVC(random_state=random_state, tol=tol, C=C,
                             penalty=penalty, loss=loss, dual=dual,
                             max_iter=max_iter))
]).fit(X_train, y_train)
#   C = 10, 5, 1, 0.5, 0.1, 0.001, 0.0001
#   penalty = 'l1', 'l2'
#   loss = 'hinge', 'squared_hinge'
#   dual = True, False
#   max_iter = 1000, 2000, 3000, 4000, 5000


# cross validation
cross_validation_report(linear_SVC, X_train, y_train)

