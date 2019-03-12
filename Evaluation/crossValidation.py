import numpy as np
from sklearn.model_selection import cross_validate


CENTER_TEXT = '{:^22s}'
TABLE_HEADER = '{:>11s}{:>11s}'
TABLE_ROW = '{:>11.3f}{:>11.3f}'
TABLE_BORDER = '-' * 22
TABLE_OUTER_BORDER = '*' * 22


def print_report(f1_macro, score):
    print(TABLE_OUTER_BORDER)
    print(CENTER_TEXT.format('CV REPORT'))
    print(TABLE_BORDER)
    print(TABLE_HEADER.format('f1 macro', 'accuracy'))
    print(TABLE_BORDER)
    print(TABLE_ROW.format(f1_macro, score))
    print(TABLE_OUTER_BORDER)


def cross_validation_report(clf, feature_sets, labels):
    cv = 3
    scoring = ['f1_macro', 'f1_micro', 'accuracy']
    n_jobs = -1
    return_train_score = False

    for feature_set in feature_sets:
        scores = cross_validate(clf, feature_set, labels,
                                scoring=scoring, cv=cv, n_jobs=n_jobs,
                                return_train_score=return_train_score)
        f1_macro = np.mean(scores['test_f1_macro'])
        score = np.mean(scores['test_accuracy'])

        print_report(f1_macro, score)
