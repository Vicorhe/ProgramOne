from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier


def random_subspaces():
    # random subspaces classifier
    base_estimator = DecisionTreeClassifier()
    n_estimators = 10
    max_samples = 1.0
    max_features = 0.5
    bootstrap = False
    bootstrap_features = True
    n_jobs = -1
    random_subspaces_clf = Pipeline([
        ('random_subspaces_clf', BaggingClassifier(base_estimator=base_estimator,
                                                   n_estimators=n_estimators,
                                                   max_samples=max_samples,
                                                   max_features=max_features,
                                                   bootstrap=bootstrap,
                                                   bootstrap_features=bootstrap_features,
                                                   n_jobs=n_jobs))
    ])
    #   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
    #   n_estimators = 10, 50, 100, 300, 500
    #   max_features = 0.25, 0.5, 0.67, 0.8

    return random_subspaces_clf
