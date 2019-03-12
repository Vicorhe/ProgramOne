from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from DATASETOPS import load_tile_data_set
from Evaluation.crossValidation import cross_validation_report
from Evaluation.performance import performance_report


# load data set
train_data, test_data, train_labels, test_labels = load_tile_data_set()


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
])
#   criterion = 'gini', entropy'
#   max_depth = 3, 4, 5
#   min_samples_leaf = 2, 3, 4


# cross validation
cross_validation_report(decision_tree_clf, train_data, train_labels)


# performance
performance_report(decision_tree_clf, train_data, train_labels,
                   test_data, test_labels)
