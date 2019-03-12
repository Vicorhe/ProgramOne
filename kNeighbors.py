from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# k nearest neighbors classifier
n_neighbors = 3
weights = 'uniform'

k_nearest_neighbors_clf = Pipeline([
    ('k_nearest_neighbors_clf', KNeighborsClassifier(n_neighbors=n_neighbors,
                                                     weights=weights))
])
#   n_neighbors: 3, 5, 7, 9, 11
#   weights: 'uniform', 'distance'


# cross validation
cross_validation_report(k_nearest_neighbors_clf, train_data, train_labels)


# performance
performance_report(k_nearest_neighbors_clf, train_data, train_labels,
                   test_data, test_labels)
