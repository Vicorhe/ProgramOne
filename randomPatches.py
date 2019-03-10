from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from Modules.DataSetOperations import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from Modules.FeatureExtraction.feature_set_b import get_statistics
from Modules.Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


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
]).fit(X_train, y_train)
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_samples = 0.25, 0.5, 0.67, 0.8
#   max_features = 0.25, 0.5, 0.67, 0.8
#   bootstrap = True, False


# cross validation
cross_validation_report(random_patches_clf, X_train, y_train)
