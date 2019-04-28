from sklearn.pipeline import Pipeline
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier


def get_classifier():
    # ada boost classifier
    base_estimator = DecisionTreeClassifier(max_depth=1)
    n_estimators = 50
    learning_rate = 0.25
    algorithm = 'SAMME.R'
    ada_boost_clf = Pipeline([
        ('ada_boost_clf', AdaBoostClassifier(base_estimator=base_estimator,
                                             n_estimators=n_estimators,
                                             learning_rate=learning_rate,
                                             algorithm=algorithm))
    ])
    # base_estimator = DecisionTreeClassifier(max_depth=1)
    # n_estimators = 25, 50, 100, 200
    # learning_rate = 0.25, 0.5, 1., 1.5
    # algorithm = 'SAMME’, ‘SAMME.R'

    return ada_boost_clf
