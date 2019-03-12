from sklearn.pipeline import Pipeline
from sklearn.linear_model import Perceptron
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# perceptron classifier
penalty = None
max_iter = 1000
tol = 1e-3
eta0 = 1
n_jobs = -1
early_stopping = False
perceptron_clf = Pipeline([
    ('perceptron_clf', Perceptron(penalty=penalty, max_iter=max_iter, tol=tol,
                                  eta0=eta0, n_jobs=n_jobs,
                                  early_stopping=early_stopping))
])
#   penalty = None, 'l2', 'l1', 'elasticnet'
#   alpha = 0.0001
#   max_iter = 1000, 2000
#   tol = 1e-3, 1e-4, 1e-5
#   eta0 = 1
#   early_stopping = False, True
#   validation_fraction = 0.1, 0.2, 0.15
#   n_iter_no_change = 5, 6, 7


# cross validation
cross_validation_report(perceptron_clf, train_data, train_labels)


# performance
performance_report(perceptron_clf, train_data, train_labels,
                   test_data, test_labels)
