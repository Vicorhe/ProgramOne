from numpy import mean
from sklearn.base import clone


ROW = '{:>5s}:{:>8.3f}'


def performance_report(clf, train_feature_sets, train_labels,
                       test_feature_sets, test_labels):
    scores = list()
    for i, (train_set, test_set) in enumerate(zip(train_feature_sets,
                                                  test_feature_sets)):
        clone_clf = clone(clf)
        clone_clf.fit(train_set, train_labels)
        accuracy = clone_clf.score(test_set, test_labels)
        scores.append(accuracy)
    print(ROW.format('PERF', mean(scores)))

