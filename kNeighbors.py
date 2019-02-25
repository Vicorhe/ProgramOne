from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from Datasets.utils import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)

# k nearest neighbors classifier

n_neighbors = 3
weights = 'uniform'
k_nearest_neighbors_clf = Pipeline([
    ('k_nearest_neighbors_clf', KNeighborsClassifier(n_neighbors=n_neighbors,
                                                     weights=weights))
])
#   n_neighbors: 3, 5, 7, 9, 11
#   weights: 'uniform', 'distance'

k_nearest_neighbors_clf.fit(X_train, y_train)

# cross validation
cross_validation_report(k_nearest_neighbors_clf, X_train, y_train)
