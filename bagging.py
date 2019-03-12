from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# bagging classifier
base_estimator = DecisionTreeClassifier()
n_estimators = 10
max_samples = 0.25
bootstrap = True
oob_score = True
n_jobs = -1
bagging_clf = Pipeline([
    ('bagging_clf', BaggingClassifier(base_estimator=base_estimator,
                                      n_estimators=n_estimators,
                                      max_samples=max_samples,
                                      bootstrap=bootstrap,
                                      oob_score=oob_score,
                                      n_jobs=n_jobs))
])
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_samples = 0.25, 0.5, 0.67, 0.8


# cross validation
cross_validation_report(bagging_clf, train_data, train_labels)


# performance
performance_report(bagging_clf, train_data, train_labels,
                   test_data, test_labels)
