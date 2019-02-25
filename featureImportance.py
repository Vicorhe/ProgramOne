from sklearn.ensemble import RandomForestClassifier
from Datasets.utils import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics, get_feature_names
from FeatureExtraction.feature_set_b import get_statistics, get_feature_names


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# random forest ensemble classifier

n_estimators = 500
max_leaf_nodes = 16
n_jobs = -1

random_forest_clf = RandomForestClassifier(n_estimators=n_estimators,
                                           max_leaf_nodes=max_leaf_nodes,
                                           n_jobs=n_jobs)
random_forest_clf.fit(X_train, y_train)


feature_importance = zip(get_feature_names(),
                         random_forest_clf.feature_importances_)

for name, score in sorted(feature_importance, key=lambda x : x[1], reverse=True):
    print('{:>11s}{:10.4f}'.format(name, score))
