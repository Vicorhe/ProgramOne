from sklearn.pipeline import Pipeline
from sklearn.neighbors import RadiusNeighborsClassifier
from DATASETOPS import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set()


# radius neighbors classifier

radius = 5000.0

radius_neighbors_clf = Pipeline([
    ('radius_neighbors_clf', RadiusNeighborsClassifier(radius=radius, weights='uniform'))
]).fit(X_train, y_train)
#   consider normalizing
#   radius: 5000 ...
#   weights: 'uniform', 'distance'


# cross validate
cross_validation_report(radius_neighbors_clf, X_train, y_train)

