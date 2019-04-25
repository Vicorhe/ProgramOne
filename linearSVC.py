from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
# from DATASETOPS import load_tile_data_set
from livetraining import get_data
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = get_data()


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
])
#   C = 10, 5, 1, 0.5, 0.1, 0.001, 0.0001
#   penalty = 'l1', 'l2'
#   loss = 'hinge', 'squared_hinge'
#   dual = True, False
#   max_iter = 1000, 2000, 3000, 4000, 5000


# cross validation
cross_validation_report(linear_SVC, train_data, train_labels, False)


# performance
performance_report(linear_SVC, train_data, train_labels,
                   test_data, test_labels, False)
