from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# random forest classifier
n_estimators = 10
criterion = 'gini'
max_depth = 4
max_features = 'sqrt'
bootstrap = True
n_jobs = -1
random_forest_clf = Pipeline([
    ('random_forest_clf', RandomForestClassifier(n_estimators=n_estimators,
                                                 criterion=criterion,
                                                 max_depth=max_depth,
                                                 max_features=max_features,
                                                 bootstrap=bootstrap,
                                                 n_jobs=n_jobs))
])
#   n_estimators = 10, 50, 100, 300, 500
#   criterion = 'gini', 'entropy'
#   max_depth = 2, 4, 6, 8, 10
#   max_features = 'sqrt', 'log2', None


# cross validation
cross_validation_report(random_forest_clf, train_data, train_labels)


# performance
performance_report(random_forest_clf, train_data, train_labels,
                   test_data, test_labels)
