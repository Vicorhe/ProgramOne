from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from DATASETOPS import load_tile_data_set
# from FeatureExtraction.feature_set_b import get_statistics
from Evaluation.crossValidation import cross_validation_report


# load data set
X_train, y_train, X_test, y_test = load_tile_data_set()


# decision tree classifier

criterion = 'gini'
max_depth = 3
min_samples_leaf = 4
random_state = 6117
presort = True

decision_tree_clf = Pipeline([
    ('decision_tree_clf', DecisionTreeClassifier(criterion=criterion,
                                                 max_depth=max_depth,
                                                 min_samples_leaf=min_samples_leaf,
                                                 random_state=random_state,
                                                 presort=presort))
]).fit(X_train, y_train)
#   criterion = 'gini', entropy'
#   max_depth = 3, 4, 5
#   min_samples_leaf = 2, 3, 4


# cross validation
cross_validation_report(decision_tree_clf, X_train, y_train)

