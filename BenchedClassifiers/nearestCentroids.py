from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestCentroid
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


# nearest centroids classifier
nearest_centroid_clf = Pipeline([
    ('nearest_centroids_clf', NearestCentroid())
])
#   shrink_threshold: 0.2


# cross validation
cross_validation_report(nearest_centroid_clf, train_data, train_labels)


# performance
performance_report(nearest_centroid_clf, train_data, train_labels,
                   test_data, test_labels)
