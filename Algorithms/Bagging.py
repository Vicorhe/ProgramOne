from sklearn.pipeline import Pipeline
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier


def bagging():
    # bagging classifier
    base_estimator = DecisionTreeClassifier()
    n_estimators = 10
    max_samples = 0.25
    bootstrap = True
    oob_score = True
    n_jobs = -1
    bagging_clf = Pipeline([
        ('bagging_clf', BaggingClassifier(base_estimator=base_estimator,
                                          n_estimators=n_estimators,
                                          max_samples=max_samples,
                                          bootstrap=bootstrap,
                                          oob_score=oob_score,
                                          n_jobs=n_jobs))
    ])
    #   base_estimator = DecisionTreeClassifier(), SVC(), KNeighborsClassifier()
    #   n_estimators = 10, 50, 100, 300, 500
    #   max_samples = 0.25, 0.5, 0.67, 0.8

    return bagging_clf
