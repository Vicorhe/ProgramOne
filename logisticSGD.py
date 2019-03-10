from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from Modules.DataSetOperations import load_tile_data_set
from Modules.FeatureExtraction.feature_set_a import get_statistics
# from FeatureExtraction.feature_set_b import get_statistics
from Modules.Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# log loss stochastic gradient descent classifier

loss = 'log'
penalty = 'l2'
max_iter = 1000
n_jobs = -1
random_state = 6117


SGD_clf = Pipeline([
    ('SGD', SGDClassifier(loss=loss, penalty=penalty, max_iter=max_iter,
                          n_jobs=n_jobs, random_state=random_state))
]).fit(X_train, y_train)
#   loss = 'hinge', 'log', 'modified_huber'
#   penalty = 'l1', 'l2', 'elasticnet'
#   max_iter = 1000, 2000, 3000, 4000, 5000


# cross validation
cross_validation_report(SGD_clf, X_train, y_train)

