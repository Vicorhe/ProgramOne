from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from Datasets.utils import load_tile_data_set
# from FeatureExtraction.feature_set_a import get_statistics
from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# pasting classifier

base_estimator = DecisionTreeClassifier()
n_estimators = 10
max_samples = 0.25
bootstrap = False
n_jobs = -1

pasting_clf = Pipeline([
    ('pasting_clf', BaggingClassifier(base_estimator=base_estimator,
                                      n_estimators=n_estimators,
                                      max_samples=max_samples,
                                      bootstrap=bootstrap,
                                      n_jobs=n_jobs))
]).fit(X_train, y_train)
#   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
#   n_estimators = 10, 50, 100, 300, 500
#   max_samples = 0.25, 0.5, 0.67, 0.8


# cross validation
cross_validation_report(pasting_clf, X_train, y_train)
