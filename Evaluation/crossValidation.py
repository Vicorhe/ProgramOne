from numpy import mean
from sklearn.model_selection import cross_validate


ROW = 'CV MEAN:{:>8.3f}   MAX:{:>8.3f}   MIN:{:>8.3f}'
NUM_RUNS = 5


def cross_validation_report(clf, feature_sets, labels):
    meta_stats = list()
    cv = 3
    scoring = ['accuracy']
    n_jobs = -1
    return_train_score = False

    for i in range(NUM_RUNS):
        scores = list()
        for feature_set in feature_sets:
            c_v = cross_validate(clf, feature_set, labels, scoring=scoring, cv=cv,
                                 n_jobs=n_jobs, return_train_score=return_train_score)
            accuracy = mean(c_v['test_accuracy'])
            scores.append(accuracy)
        meta_stats.append(mean(scores))

    print(ROW.format(mean(meta_stats), max(meta_stats), min(meta_stats)))
