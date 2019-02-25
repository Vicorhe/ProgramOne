import numpy as np
from sklearn.model_selection import cross_validate


CENTER_TEXT = '{:^35s}'
TABLE_HEADER = '{:>11s}{:>11s}{:>11s}'
TABLE_ROW = '{:>11.3f}{:>11.3f}{:>11.3f}'
TABLE_BORDER = '-' * 33


def cross_validation_report(clf, data, labels):
    cv = 4
    scoring = ['f1_macro', 'f1_micro', 'accuracy']
    n_jobs = -1
    return_train_score = False
    scores = cross_validate(clf, data, labels,
                            scoring=scoring, cv=cv, n_jobs=n_jobs,
                            return_train_score=return_train_score)
    f1_macro = np.mean(scores['test_f1_macro'])
    f1_micro = np.mean(scores['test_f1_micro'])
    score = np.mean(scores['test_accuracy'])

    print(TABLE_BORDER)

    print(CENTER_TEXT.format('CROSS EVALUATION REPORT'))

    print(TABLE_BORDER)

    print(TABLE_HEADER.format('macro f1', 'micro f1', 'accuracy'))

    print(TABLE_BORDER)

    print(TABLE_ROW.format(f1_macro, f1_micro, score))

    print(TABLE_BORDER)
