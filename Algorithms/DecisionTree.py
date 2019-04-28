from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


def get_classifier():
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

    return decision_tree_clf
