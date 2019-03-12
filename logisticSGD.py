from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# log loss stochastic gradient descent classifier
loss = 'log'
penalty = 'l2'
max_iter = 1000
n_jobs = -1
random_state = 6117
SGD_clf = Pipeline([
    ('SGD', SGDClassifier(loss=loss, penalty=penalty, max_iter=max_iter,
                          n_jobs=n_jobs, random_state=random_state))
])
#   loss = 'hinge', 'log', 'modified_huber'
#   penalty = 'l1', 'l2', 'elasticnet'
#   max_iter = 1000, 2000, 3000, 4000, 5000


# cross validation
cross_validation_report(SGD_clf, train_data, train_labels)


# performance
performance_report(SGD_clf, train_data, train_labels,
                   test_data, test_labels)
