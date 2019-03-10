from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from Modules.DataSetOperations import load_tile_data_set
from Modules.FeatureExtraction.feature_set_a import get_statistics
# from FeatureExtraction.feature_set_b import get_statistics
from Modules.Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set(feature_func=get_statistics)


# ada boost classifier

base_estimator = DecisionTreeClassifier(max_depth=1)
n_estimators = 50
learning_rate = 1.
algorithm = 'SAMME.R'

ada_boost_clf = Pipeline([
    ('ada_boost_clf', AdaBoostClassifier(base_estimator=base_estimator,
                                         n_estimators=n_estimators,
                                         learning_rate=learning_rate,
                                         algorithm=algorithm))
]).fit(X_train, y_train)
#   base_estimator = DecisionTreeClassifier(max_depth=1)
#   n_estimators = 25, 50, 100, 200
#   learning_rate = 0.25, 0.5, 1., 1.5
#   algorithm = 'SAMME’, ‘SAMME.R'


# cross validation
cross_validation_report(ada_boost_clf, X_train, y_train)
