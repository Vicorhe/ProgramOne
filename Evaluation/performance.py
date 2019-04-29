from numpy import mean
from sklearn.base import clone


def performance_report(clf, train_feature_sets, train_labels,
                       test_feature_sets, test_labels):
    scores = list()
    for train_set, test_set in zip(train_feature_sets, test_feature_sets):
        clone_clf = clone(clf)
        clone_clf.fit(train_set, train_labels)
        accuracy = clone_clf.score(test_set, test_labels)
        scores.append(accuracy)
    print("%.3f" % mean(scores))
