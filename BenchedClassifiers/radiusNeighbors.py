from sklearn.pipeline import Pipeline
from sklearn.neighbors import RadiusNeighborsClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# radius neighbors classifier
radius = 5000.0
radius_neighbors_clf = Pipeline([
    ('radius_neighbors_clf', RadiusNeighborsClassifier(radius=radius, weights='uniform'))
])
#   consider normalizing
#   radius: 5000 ...
#   weights: 'uniform', 'distance'


# cross validate
cross_validation_report(radius_neighbors_clf, train_data, train_labels)


# performance
performance_report(radius_neighbors_clf, train_data, train_labels,
                   test_data, test_labels)
