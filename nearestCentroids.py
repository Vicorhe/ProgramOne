from sklearn.pipeline import Pipeline
from sklearn.neighbors import NearestCentroid
from Datasets.utils import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# nearest centroids classifier

nearest_centroid_clf = Pipeline([
    ('nearest_centroids_clf', NearestCentroid())
]).fit(X_train, y_train)
#   shrink_threshold: 0.2


# cross validation
cross_validation_report(nearest_centroid_clf, X_train, y_train)
