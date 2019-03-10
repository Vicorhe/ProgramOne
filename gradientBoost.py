from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from DATASETOPS import load_tile_data_set
# from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set()


# gradient boost classifier

loss = 'deviance'
learning_rate = 0.1
n_estimators = 100
subsample = 1.0
criterion = 'friedman_mse'
max_depth = 3
max_features = 'sqrt'

gradient_boost_clf = Pipeline([
    ('ada_boost_clf', GradientBoostingClassifier(loss=loss,
                                                 learning_rate=learning_rate,
                                                 n_estimators=n_estimators,
                                                 subsample=subsample,
                                                 criterion=criterion,
                                                 max_depth=max_depth,
                                                 max_features=max_features))
]).fit(X_train, y_train)
#   loss = 'deviance', 'exponential'
#   learning_rate = 0.1, 0.2, 0.3, 0.5, 0.7, 1.0
#   n_estimators = 25, 50, 100, 200
#   subsample = 0.1, 0.25, 0.5, 0.75, 1.0
#   criterion = 'friedman_mse', 'mse', 'mae'
#   max_depth = 2, 4, 6, 8, 10
#   max_features = 'sqrt', 'log2', None


# cross validation
cross_validation_report(gradient_boost_clf, X_train, y_train)
