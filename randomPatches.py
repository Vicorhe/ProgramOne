from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# random patches classifier
base_estimator = DecisionTreeClassifier()
n_estimators = 10
max_samples = 0.5
max_features = 0.5
bootstrap = True
bootstrap_features = True
oob_score = True
n_jobs = -1
random_patches_clf = Pipeline([
    ('random_patches_clf', BaggingClassifier(base_estimator=base_estimator,
                                             n_estimators=n_estimators,
                                             max_samples=max_samples,
                                             max_features=max_features,
                                             bootstrap=bootstrap,
                                             bootstrap_features=bootstrap_features,
                                             oob_score=oob_score,
                                             n_jobs=n_jobs))
])
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_samples = 0.25, 0.5, 0.67, 0.8
#   max_features = 0.25, 0.5, 0.67, 0.8
#   bootstrap = True, False


# cross validation
cross_validation_report(random_patches_clf, train_data, train_labels)


# performance
performance_report(random_patches_clf, train_data, train_labels,
                   test_data, test_labels)
