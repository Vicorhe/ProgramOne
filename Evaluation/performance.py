from numpy import mean
from sklearn.base import clone


ROW = 'P  MEAN:{:>8.3f}   MAX:{:>8.3f}   MIN:{:>8.3f}'
NUM_RUNS = 5


def performance_report(clf, train_feature_sets, train_labels,
                       test_feature_sets, test_labels):
    meta_stats = list()
    for i in range(NUM_RUNS):
        scores = list()
        for train_set, test_set in zip(train_feature_sets, test_feature_sets):
            clone_clf = clone(clf)
            clone_clf.fit(train_set, train_labels)
            accuracy = clone_clf.score(test_set, test_labels)
            scores.append(accuracy)
        meta_stats.append(mean(scores))

    print(ROW.format(mean(meta_stats), max(meta_stats), min(meta_stats)))

