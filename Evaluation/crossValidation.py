from numpy import mean
from sklearn.model_selection import cross_validate


def cross_validation_report(clf, feature_sets, labels):
    cv = 3
    scoring = ['accuracy']
    n_jobs = -1
    return_train_score = False
    scores = list()
    for feature_set in feature_sets:
        c_v = cross_validate(clf, feature_set, labels, scoring=scoring, cv=cv,
                             n_jobs=n_jobs, return_train_score=return_train_score)
        accuracy = mean(c_v['test_accuracy'])
        scores.append(accuracy)
    print("%.3f" % mean(scores))
